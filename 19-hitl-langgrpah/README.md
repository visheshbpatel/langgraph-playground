# Human-in-the-Loop (HITL)

## Key Theory

**Human-in-the-Loop (HITL)** allows a LangGraph workflow to **pause and wait for human input before continuing**.

It is useful when an action is sensitive, requires approval, or should not happen completely autonomously.

### Why Use HITL?

* Require human approval before important actions
* Allow humans to review or modify decisions
* Prevent potentially harmful or irreversible actions from happening automatically
* Combine **AI automation with human control**

## Core Concepts

| Concept               | What you should understand                                        |
| --------------------- | ----------------------------------------------------------------- |
| **HITL**              | Human participates in the workflow at a defined point             |
| `interrupt()`         | Pauses graph execution and waits for external human input         |
| `Command`             | Used to control/resume graph execution                            |
| `Command(resume=...)` | Resumes an interrupted graph with the human's decision            |
| `__interrupt__`       | Returned information indicating that execution was interrupted    |
| `interrupt.value`     | Contains the value/message passed to `interrupt()`                |
| **Checkpointer**      | Preserves graph state while execution is paused                   |
| `thread_id`           | Identifies the execution so it can be resumed correctly           |
| **Resume**            | Continue execution from the point where the graph was interrupted |

## HITL Flow

```text
User Request
     ↓
LLM
     ↓
Tool
     ↓
interrupt()
     ↓
┌─────────────────┐
│ Human Decision  │
│   Yes / No      │
└────────┬────────┘
         ↓
Command(resume=decision)
         ↓
Continue Graph
         ↓
Final Result
```

## `interrupt()`

The workflow can pause inside a node/tool:

```python
decision = interrupt(
    f"Approve buying {quantity} shares of {symbol}? (yes/no)"
)
```

At this point, LangGraph stops execution and returns control to the caller. 

The human's decision is **not hardcoded into the graph**. It is supplied externally when the workflow is resumed.

## Detecting an Interrupt

After invoking the graph:

```python
result = chatbot.invoke(
    state,
    config={"configurable": {"thread_id": thread_id}}
)

interrupts = result.get("__interrupt__", [])
```

If an interrupt exists, the application can present it to the human. 

## Resuming with `Command`

After receiving the human decision:

```python
result = chatbot.invoke(
    Command(resume=decision),
    config={"configurable": {"thread_id": thread_id}}
)
```

`Command(resume=...)` tells LangGraph:

> **Resume the interrupted execution using this value.**



## HITL + Tools + Persistence

This combines several concepts learned previously:

```text
LLM
 ↓
Tool Calling
 ↓
ToolNode
 ↓
Sensitive Action
 ↓
interrupt()
 ↓
Checkpointed State
 ↓
Human Decision
 ↓
Command(resume=...)
 ↓
Continue Tool
 ↓
Result
```

The workflow uses `MemorySaver()` as the checkpointer, allowing the interrupted execution to retain its state while waiting for the human decision. 

### Mental Model

**`interrupt()` = Pause**

**Checkpointer = Remember where we paused**

**Human = Decide**

**`Command(resume=...)` = Continue**

**HITL = AI automation + human control**
# Human-in-the-Loop (HITL)

## Key Theory

**Human-in-the-Loop (HITL)** allows a LangGraph workflow to **pause and wait for human input before continuing**.

It is useful when an action is sensitive, requires approval, or should not happen completely autonomously.

### Why Use HITL?

* Require human approval before important actions
* Allow humans to review or modify decisions
* Prevent potentially harmful or irreversible actions from happening automatically
* Combine **AI automation with human control**

## Core Concepts

| Concept               | What you should understand                                        |
| --------------------- | ----------------------------------------------------------------- |
| **HITL**              | Human participates in the workflow at a defined point             |
| `interrupt()`         | Pauses graph execution and waits for external human input         |
| `Command`             | Used to control/resume graph execution                            |
| `Command(resume=...)` | Resumes an interrupted graph with the human's decision            |
| `__interrupt__`       | Returned information indicating that execution was interrupted    |
| `interrupt.value`     | Contains the value/message passed to `interrupt()`                |
| **Checkpointer**      | Preserves graph state while execution is paused                   |
| `thread_id`           | Identifies the execution so it can be resumed correctly           |
| **Resume**            | Continue execution from the point where the graph was interrupted |

## HITL Flow

```text
User Request
     ↓
LLM
     ↓
Tool
     ↓
interrupt()
     ↓
┌─────────────────┐
│ Human Decision  │
│   Yes / No      │
└────────┬────────┘
         ↓
Command(resume=decision)
         ↓
Continue Graph
         ↓
Final Result
```

## `interrupt()`

The workflow can pause inside a node/tool:

```python
decision = interrupt(
    f"Approve buying {quantity} shares of {symbol}? (yes/no)"
)
```

At this point, LangGraph stops execution and returns control to the caller. 

The human's decision is **not hardcoded into the graph**. It is supplied externally when the workflow is resumed.

## Detecting an Interrupt

After invoking the graph:

```python
result = chatbot.invoke(
    state,
    config={"configurable": {"thread_id": thread_id}}
)

interrupts = result.get("__interrupt__", [])
```

If an interrupt exists, the application can present it to the human. 

## Resuming with `Command`

After receiving the human decision:

```python
result = chatbot.invoke(
    Command(resume=decision),
    config={"configurable": {"thread_id": thread_id}}
)
```

`Command(resume=...)` tells LangGraph:

> **Resume the interrupted execution using this value.**



## HITL + Tools + Persistence

This combines several concepts learned previously:

```text
LLM
 ↓
Tool Calling
 ↓
ToolNode
 ↓
Sensitive Action
 ↓
interrupt()
 ↓
Checkpointed State
 ↓
Human Decision
 ↓
Command(resume=...)
 ↓
Continue Tool
 ↓
Result
```

The workflow uses `MemorySaver()` as the checkpointer, allowing the interrupted execution to retain its state while waiting for the human decision. 

### Mental Model

**`interrupt()` = Pause**

**Checkpointer = Remember where we paused**

**Human = Decide**

**`Command(resume=...)` = Continue**

**HITL = AI automation + human control**
# Human-in-the-Loop (HITL)

## Key Theory

**Human-in-the-Loop (HITL)** allows a LangGraph workflow to **pause and wait for human input before continuing**.

It is useful when an action is sensitive, requires approval, or should not happen completely autonomously.

### Why Use HITL?

* Require human approval before important actions
* Allow humans to review or modify decisions
* Prevent potentially harmful or irreversible actions from happening automatically
* Combine **AI automation with human control**

## Core Concepts

| Concept               | What you should understand                                        |
| --------------------- | ----------------------------------------------------------------- |
| **HITL**              | Human participates in the workflow at a defined point             |
| `interrupt()`         | Pauses graph execution and waits for external human input         |
| `Command`             | Used to control/resume graph execution                            |
| `Command(resume=...)` | Resumes an interrupted graph with the human's decision            |
| `__interrupt__`       | Returned information indicating that execution was interrupted    |
| `interrupt.value`     | Contains the value/message passed to `interrupt()`                |
| **Checkpointer**      | Preserves graph state while execution is paused                   |
| `thread_id`           | Identifies the execution so it can be resumed correctly           |
| **Resume**            | Continue execution from the point where the graph was interrupted |

## HITL Flow

```text
User Request
     ↓
LLM
     ↓
Tool
     ↓
interrupt()
     ↓
┌─────────────────┐
│ Human Decision  │
│   Yes / No      │
└────────┬────────┘
         ↓
Command(resume=decision)
         ↓
Continue Graph
         ↓
Final Result
```

## `interrupt()`

The workflow can pause inside a node/tool:

```python
decision = interrupt(
    f"Approve buying {quantity} shares of {symbol}? (yes/no)"
)
```

At this point, LangGraph stops execution and returns control to the caller. 

The human's decision is **not hardcoded into the graph**. It is supplied externally when the workflow is resumed.

## Detecting an Interrupt

After invoking the graph:

```python
result = chatbot.invoke(
    state,
    config={"configurable": {"thread_id": thread_id}}
)

interrupts = result.get("__interrupt__", [])
```

If an interrupt exists, the application can present it to the human. 

## Resuming with `Command`

After receiving the human decision:

```python
result = chatbot.invoke(
    Command(resume=decision),
    config={"configurable": {"thread_id": thread_id}}
)
```

`Command(resume=...)` tells LangGraph:

> **Resume the interrupted execution using this value.**



## HITL + Tools + Persistence

This combines several concepts learned previously:

```text
LLM
 ↓
Tool Calling
 ↓
ToolNode
 ↓
Sensitive Action
 ↓
interrupt()
 ↓
Checkpointed State
 ↓
Human Decision
 ↓
Command(resume=...)
 ↓
Continue Tool
 ↓
Result
```

The workflow uses `MemorySaver()` as the checkpointer, allowing the interrupted execution to retain its state while waiting for the human decision. 

### Mental Model

**`interrupt()` = Pause**

**Checkpointer = Remember where we paused**

**Human = Decide**

**`Command(resume=...)` = Continue**

**HITL = AI automation + human control**
