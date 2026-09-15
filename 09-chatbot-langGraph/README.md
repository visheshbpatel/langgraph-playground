# Lesson 9 — Stateful Chatbot

## Key Theory

A **stateful chatbot** maintains conversation history across multiple graph invocations.

LangGraph achieves this using **message state + reducers + checkpointing + thread IDs**.

```text
User Message
     ↓
  Chat Node
     ↓
Update State
     ↓
Checkpoint
     ↓
Next Invocation
     ↓
Restore State
     ↓
  Chat Node
```

## New Concepts

| Concept                 | What you should understand                                                                                   |
| ----------------------- | ------------------------------------------------------------------------------------------------------------ |
| `TypedDict`             | Defines the expected structure and types of the graph state                                                  |
| `BaseMessage`           | Base type for `HumanMessage`, `AIMessage`, `SystemMessage`, etc.                                             |
| `Annotated`             | Attaches additional behavior/metadata to a state field                                                       |
| `add_messages`          | Reducer that combines new messages with existing message history                                             |
| **Message state**       | Stores the conversation as a list of messages                                                                |
| **State update**        | A node can return only the fields it wants to update                                                         |
| `StateGraph(ChatState)` | Defines a graph that operates using `ChatState`                                                              |
| `MemorySaver()`         | In-memory checkpointer that stores graph checkpoints while the process is running                            |
| **Checkpointer**        | Saves graph state so it can be retrieved or resumed later                                                    |
| **Thread ID**           | Identifies a particular conversation/state history                                                           |
| `config`                | Provides runtime configuration such as the `thread_id`                                                       |
| `get_state()`           | Retrieves the checkpointed state for a given thread                                                          |
| `compile()`             | Converts the graph definition into an executable workflow and attaches infrastructure such as a checkpointer |
| `invoke()`              | Executes the compiled graph with an input state                                                              |

## Message State & Reducer

```python
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
```

The state contains a list of messages:

```text
[HumanMessage, AIMessage, HumanMessage, AIMessage, ...]
```

When a node returns:

```python
{"messages": [response]}
```

`add_messages` determines how the new messages are combined with the existing message history.

```text
Existing Messages
        +
New Messages
        ↓
    add_messages
        ↓
Updated Message History
```

## Checkpointing & Threads

A checkpointer is attached during compilation:

```python
checkpointer = MemorySaver()

chatbot = graph.compile(
    checkpointer=checkpointer
)
```

The checkpointer is **not a node** in the graph. It is infrastructure that saves graph state.

A `thread_id` identifies which saved state history belongs to an invocation:

```python
config = {
    "configurable": {
        "thread_id": "1"
    }
}
```

Using the same thread:

```text
thread_id = "1"
      ↓
Conversation A
      ↓
Saved State
      ↓
Next invocation
      ↓
Same Conversation A
```

A different thread represents a separate state history:

```text
thread "1" → Conversation A
thread "2" → Conversation B
```

## Execution Flow

```text
Define State
     ↓
Create StateGraph
     ↓
Add Nodes & Edges
     ↓
Compile + Checkpointer
     ↓
Invoke with Input
     ↓
Execute Graph
     ↓
Update State
     ↓
Save Checkpoint
```

For a stateful chatbot:

```text
Input + thread_id
       ↓
Restore checkpoint
       ↓
Merge new message
       ↓
Chat Node
       ↓
Update messages
       ↓
Save checkpoint
```

## Main Learning

> **State tells the graph what it knows, while checkpointing allows that state to persist between invocations.**

The key mental model:

> **State = Data | Reducer = State Update Rule | Checkpointer = Save State | Thread ID = State History Identity | Config = Runtime Context**

### Important Distinction

```text
State
→ What the graph currently knows

Checkpointer
→ Where/how graph state is saved

Thread ID
→ Which saved state history to use
```

`compile()` prepares the graph for execution; `invoke()` actually runs it.
