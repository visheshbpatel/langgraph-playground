# 10. Persistence


Persistence allows a LangGraph workflow to **save and retrieve execution state through checkpoints**.

Instead of only keeping the final result, LangGraph can maintain a history of the workflow's state at different execution points. This makes it possible to inspect previous states, resume from a checkpoint, and create new branches from earlier states.

## Core Concepts

| Concept               | What you should understand                                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `InMemorySaver()`     | An in-memory checkpointer that stores checkpoints in RAM                                                                 |
| Persistence           | Saving workflow execution state so it can be retrieved later                                                             |
| Checkpoint            | A saved snapshot of the graph's state and execution position                                                             |
| `StateSnapshot`       | Object containing information about a checkpoint, including state values, next nodes, configuration, metadata, and tasks |
| `thread_id`           | Identifies a particular execution/history so different conversations can maintain separate state                         |
| `checkpoint_id`       | Identifies a specific checkpoint within a thread                                                                         |
| `get_state()`         | Retrieves the current or specified checkpoint state                                                                      |
| `get_state_history()` | Retrieves the sequence of checkpoints for a thread                                                                       |
| `update_state()`      | Creates a new state/checkpoint based on an existing checkpoint                                                           |
| Time Travel           | Retrieving an earlier checkpoint and continuing execution from that point                                                |
| Forking               | Creating a new execution path from an existing checkpoint                                                                |
| State History         | The timeline of how the graph's state changed during execution                                                           |

## Partial State Updates

A node does **not** need to return the entire state.

For example:

```python
class JokeState(TypedDict):
    topic: str
    joke: str
    explanation: str
```

The `generate_joke` node can return:

```python
return {"joke": response}
```

LangGraph applies this as a **state update**:

```text
Before:
{
    topic: "AI",
    joke: "",
    explanation: ""
}

        ↓ generate_joke

After:
{
    topic: "AI",
    joke: "AI walks into a bar...",
    explanation: ""
}
```

The other fields remain unchanged.

### Important Mental Model

> **Node returns an update → LangGraph applies that update to the existing state.**

This means the state schema describes the complete state, while individual nodes usually update only the fields they are responsible for.

---

## How State Reaches a Node

When we write:

```python
def generate_joke(state: JokeState):
```

the `state` is supplied by the **LangGraph runtime**.

The graph registers the function:

```python
graph.add_node("generate_joke", generate_joke)
```

When the workflow executes, LangGraph conceptually does:

```text
Current State
      ↓
LangGraph Runtime
      ↓
generate_joke(current_state)
      ↓
State Update
      ↓
LangGraph applies update
```

The graph object itself does not manually pass the state to the function.

### Mental Model

* `StateGraph` → defines the state schema and graph structure
* Nodes → define the work
* Runtime → executes nodes and supplies the current state
* Node → returns a state update
* Runtime → applies the update and continues execution

---

## `START` and `END`

`START` and `END` are special graph-level markers.

```python
graph.add_edge(START, "generate_joke")
graph.add_edge("generate_explanation", END)
```

They define where execution begins and where it terminates.

```text
START
  ↓
generate_joke
  ↓
generate_explanation
  ↓
END
```

| Marker  | Purpose                                |
| ------- | -------------------------------------- |
| `START` | Entry point of the graph               |
| `END`   | Signals that the workflow has finished |

They are not normal application nodes. They define the **boundaries of graph execution**.

---

## Where Checkpoints Are Created

Checkpointing is handled automatically by the LangGraph runtime when a checkpointer is attached:

```python
checkpointer = InMemorySaver()

workflow = graph.compile(
    checkpointer=checkpointer
)
```

You do **not** manually call the checkpointer after every node.

Conceptually, execution looks like:

```text
Input
  ↓
Checkpoint
  ↓
generate_joke
  ↓
Checkpoint
  ↓
generate_explanation
  ↓
Checkpoint
  ↓
END
```

More precisely, LangGraph uses a **super-step execution model**. Checkpoints are created at execution boundaries, and a super-step can contain multiple nodes when the graph executes work in parallel.

For a simple sequential graph, the checkpoint history commonly appears as:

```text
Initial State
     ↓
State before/at generate_joke
     ↓
State after joke generation
     ↓
State before/at generate_explanation
     ↓
Final State
```

So avoid thinking of a checkpointer as a function manually inserted "between every Python function."

### The important idea

> **The LangGraph runtime owns checkpointing and records the workflow's state/execution progress automatically.**

---

## Checkpoint Structure

A checkpoint can contain information such as:

```text
StateSnapshot
├── values
├── next
├── config
├── metadata
├── parent_config
├── tasks
└── interrupts
```

For example:

```text
Checkpoint
├── topic = "Indian education system"
├── joke = "..."
├── explanation = "..."
├── next = ()
├── thread_id = "2"
└── checkpoint_id = "..."
```

The `next` field is particularly useful because it tells you what execution is positioned to do next.

---

## State History

You can inspect the checkpoint history:

```python
list(workflow.get_state_history(config))
```

For the joke workflow, the history can conceptually look like:

```text
Checkpoint 0
topic

      ↓

Checkpoint 1
topic + joke

      ↓

Checkpoint 2
topic + joke + explanation
```

This gives you a timeline of the workflow rather than only its final output. 

---

## Time Travel

A specific checkpoint can be retrieved using its `checkpoint_id`:

```python
workflow.get_state({
    "configurable": {
        "thread_id": "2",
        "checkpoint_id": "..."
    }
})
```

You can then invoke the workflow from that earlier checkpoint.

Conceptually:

```text
Original execution

A → B → C
    ↑
    Checkpoint


Time travel

A → B → C'
```

The workflow can produce a different result from the same earlier state because later work is executed again. The notebook demonstrates this by resuming from the checkpoint before `generate_joke`. 

---

## Updating State

You can also modify state starting from a particular checkpoint:

```python
workflow.update_state(
    config,
    {"topic": "tier-3 colleges"}
)
```

This does **not** simply overwrite the old checkpoint.

Instead, LangGraph creates a new checkpoint derived from the selected point:

```text
Old checkpoint
      │
      ├── Original execution
      │
      └── Updated state
              ↓
        New checkpoint
```

The previous history remains available, allowing the workflow to branch from an earlier state. 

---

## Persistence Flow

```text
Define State
     ↓
Create Graph
     ↓
Add Nodes + Edges
     ↓
Create Checkpointer
     ↓
Compile Graph with Checkpointer
     ↓
Invoke with thread_id
     ↓
LangGraph Runtime Executes
     ↓
State Updates + Checkpoints
     ↓
Inspect / Restore / Time Travel / Update
```


| Stateful Chatbot      | Persistence                                          |
| --------------------- | ---------------------------------------------------- |
| `State`               | Data currently known by the graph                    |
| `thread_id`           | Identifies a state history                           |
| Checkpointer          | Mechanism for saving checkpoints                     |
| Current state         | Latest checkpoint                                    |
| `get_state()`         | Inspect saved state                                  |
| `get_state_history()` | Inspect execution timeline                           |
| Checkpoint ID         | Specific point in that timeline                      |
| Time Travel           | Continue from an earlier point                       |
| `update_state()`      | Create a new state/checkpoint from an existing point |

## Important Distinction

Do not confuse these concepts:

```text
State
  = The data the graph currently knows

Checkpointer
  = The mechanism that saves/retrieves checkpoints

Thread ID
  = Identity of a particular execution history

Checkpoint ID
  = Identity of one specific checkpoint

Runtime
  = Executes the graph and manages state transitions/checkpointing
```

Also, `InMemorySaver` is **not the same thing as long-term AI memory**. It is an in-memory checkpoint storage mechanism. Its stored data exists in the running process and is lost when that process ends.

## Main Learning

> **Persistence in LangGraph is more than saving the final output. It preserves checkpoints representing the workflow's state and execution progress, allowing the graph to inspect, resume, revisit, and branch from previous states.**

### Mental Model

**State = Data**

**Node = Work**

**Edge = Flow**

**Runtime = Execution**

**Checkpointer = Saves checkpoints**

**Thread ID = Execution history**

**Checkpoint ID = Specific point**

**State History = Timeline**

**Time Travel = Resume from earlier point**

**`update_state()` = Create a new state from an existing point**
