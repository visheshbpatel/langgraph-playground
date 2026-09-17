# 11. Chatbot UI


This lesson connects the **LangGraph backend** built in the previous lesson with a **Streamlit frontend**.

The important new idea is that LangGraph handles the **conversation workflow and persistence**, while Streamlit handles the **user interface**.

```text
User
 ↓
Streamlit UI
 ↓
chatbot.invoke()
 ↓
LangGraph
 ↓
Chat Node → Checkpointer
 ↓
Response
 ↓
Streamlit UI
```

## New Concepts

| Concept                     | What you should understand                                                            |
| --------------------------- | ------------------------------------------------------------------------------------- |
| Streamlit                   | Framework used to build the chatbot's web UI                                          |
| Backend–Frontend separation | LangGraph handles workflow logic; Streamlit handles presentation and user interaction |
| `st.chat_input()`           | Creates a chat input field for the user                                               |
| `st.chat_message()`         | Displays messages in a chat-style interface                                           |
| `st.session_state`          | Streamlit's mechanism for maintaining UI state across reruns                          |
| `message_history`           | List maintained by Streamlit to display messages already shown in the UI              |
| `CONFIG`                    | Runtime configuration passed to LangGraph, containing the `thread_id`                 |
| `chatbot.invoke()`          | Sends a new user message to the LangGraph workflow                                    |
| `HumanMessage`              | Represents the user's message in LangChain's message format                           |
| `thread_id`                 | Connects multiple LangGraph invocations to the same persisted conversation            |
| Checkpointer                | Stores LangGraph execution state so the conversation can continue across invocations  |

## Backend vs Frontend State

One of the most important ideas in this lesson is that there are **two different kinds of state**.

### Streamlit State

```python
st.session_state["message_history"]
```

This is used by the frontend to remember what messages should be displayed in the UI.

### LangGraph State

```python
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
```

This is the state used by the LangGraph workflow.

```text
Streamlit
    │
    │ UI state
    ↓
message_history
    │
    │ user input
    ↓
LangGraph
    │
    │ workflow state
    ↓
ChatState
    │
    ↓
Checkpointer
```

They solve different problems.

> **Streamlit state controls what the UI displays. LangGraph state controls what the workflow knows.**

The backend defines the chatbot graph and attaches `InMemorySaver` as its checkpointer. 

---

## `thread_id` Connects the Conversation

The frontend defines:

```python
CONFIG = {
    "configurable": {
        "thread_id": "thread-1"
    }
}
```

Every invocation uses this configuration:

```python
chatbot.invoke(
    {
        "messages": [
            HumanMessage(content=user_input)
        ]
    },
    config=CONFIG
)
```

The `thread_id` tells LangGraph:

> "This invocation belongs to this particular conversation history."

So:

```text
thread-1
 ├── User message
 ├── AI response
 ├── User message
 ├── AI response
 └── ...
```

A different thread ID represents a different conversation history.

---

## Message Flow

When the user enters:

```text
What is LangGraph?
```

the frontend creates:

```python
HumanMessage(content="What is LangGraph?")
```

and sends it to the graph.

```text
User Input
    ↓
HumanMessage
    ↓
chatbot.invoke()
    ↓
ChatState.messages
    ↓
chat_node
    ↓
LLM
    ↓
AIMessage
    ↓
{"messages": [response]}
    ↓
add_messages
    ↓
Updated ChatState
    ↓
Checkpointer
    ↓
Streamlit displays response
```

The backend's `chat_node` reads the current `messages`, invokes the model, and returns the new AI message as a state update. 

---

## Why `add_messages` Matters

The state contains:

```python
messages: Annotated[list[BaseMessage], add_messages]
```

The `add_messages` reducer ensures that new messages are combined with the existing message history.

For example:

```text
Before:
[
    HumanMessage("Hello"),
    AIMessage("Hi!")
]

New update:
[
    HumanMessage("How are you?")
]

After:
[
    HumanMessage("Hello"),
    AIMessage("Hi!"),
    HumanMessage("How are you?")
]
```

Without an appropriate reducer, updating a state field can replace its previous value rather than maintaining the intended history.

---

## Persistence Benefits

Persistence is useful because it provides more than simply storing data.

### 1. Short-Term Memory

The chatbot can maintain conversation context across multiple invocations within the same thread.

```text
User: My name is Vishesh.
        ↓
AI: Nice to meet you!

User: What is my name?
        ↓
AI: Your name is Vishesh.
```

The conversation state is persisted through checkpoints and associated with the thread.

> **Short-term memory = remembering information within an ongoing conversation/thread.**

---

### 2. Fault Tolerance

If a workflow is interrupted or fails after some progress, checkpoints provide previously saved execution state.

Conceptually:

```text
Input
 ↓
Checkpoint
 ↓
Node A
 ↓
Checkpoint
 ↓
Node B  ← failure
```

The saved checkpoint can provide a known state from which execution can potentially be resumed, rather than requiring the entire workflow to start from scratch.

> **Persistence gives the workflow recoverable execution points.**

---

### 3. Human-in-the-Loop

Persistence is important when a workflow needs to **pause and wait for human input or approval**.

```text
Node A
 ↓
Checkpoint
 ↓
Human approval
 ↓
Checkpoint
 ↓
Node B
```

Because the state is persisted, the workflow can retain its progress while waiting for the human decision.

This becomes especially important for workflows involving:

* approvals
* reviewing generated content
* sensitive actions
* manual corrections
* user decisions

---

### 4. Time Travel

Because previous checkpoints are preserved, you can inspect or resume from an earlier point.

```text
Checkpoint 1
     ↓
Checkpoint 2
     ↓
Checkpoint 3
     ↓
Checkpoint 4
```

You can go back to:

```text
Checkpoint 2
```

and continue execution from there.

This can also create a different execution path.

> **Time travel = using a previous checkpoint as the starting point for another execution path.**

---

## Persistence Benefits at a Glance

| Benefit           | What persistence enables                       |
| ----------------- | ---------------------------------------------- |
| Short-Term Memory | Maintain conversation/workflow context         |
| Fault Tolerance   | Recover from saved execution points            |
| Human-in-the-Loop | Pause while retaining workflow state           |
| Time Travel       | Revisit and continue from previous checkpoints |

---


## Overall Architecture

```text
                Streamlit Frontend
                       │
              ┌────────┴────────┐
              │                 │
       st.session_state    User Input
              │                 │
              │                 ↓
              │          HumanMessage
              │                 │
              └──────────────┐  │
                             ↓  ↓
                         LangGraph
                             │
                         ChatState
                             │
                         chat_node
                             │
                            LLM
                             │
                       AIMessage
                             │
                       add_messages
                             │
                         Checkpoint
                             │
                         thread_id
                             │
                             ↓
                      Streamlit UI
```

## Main Learning

> **LangGraph manages the stateful chatbot workflow, while Streamlit provides the interface through which users interact with it.**

The important connection is:

**Streamlit UI → `HumanMessage` → `chatbot.invoke()` → LangGraph State → Checkpointer → AI response → Streamlit UI**


