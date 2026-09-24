# 14. Resumeable Chatbot

## Key Theory

A resumable chatbot allows users to maintain **multiple conversations**, switch between them, start new conversations, and restore a previous conversation using its `thread_id`.

The important idea is that **each conversation is represented by a separate LangGraph thread**.

```text
User
 ↓
Streamlit UI
 ↓
Select / Create thread
 ↓
thread_id
 ↓
LangGraph Checkpointer
 ↓
Restore conversation state
 ↓
Continue conversation
```

## What We Learned

| Concept                      | What you should understand                                                       |
| ---------------------------- | -------------------------------------------------------------------------------- |
| **Multiple Threads**         | Each conversation can have its own independent state/history                     |
| `thread_id`                  | Uniquely identifies a conversation/state history                                 |
| `uuid.uuid4()`               | Generates a unique ID for a new conversation                                     |
| `Generate_thread_id()`       | Creates a new unique thread for a new chat                                       |
| `chat_threads`               | Streamlit-side collection used to keep track of available conversations          |
| `reset_chat()`               | Creates a new thread and clears the current UI message history                   |
| `add_thread()`               | Adds a thread ID to the list of available conversations                          |
| `load_conversation()`        | Retrieves saved messages for a selected thread from LangGraph                    |
| `get_state()`                | Retrieves the current checkpointed state for a specific thread                   |
| `state.values`               | Contains the state values stored in the retrieved checkpoint                     |
| **Conversation Switching**   | Changing the `thread_id` changes which persisted conversation LangGraph accesses |
| **Conversation Restoration** | Previously checkpointed messages can be loaded back into the UI                  |
| **Thread Isolation**         | Different thread IDs represent separate conversation histories                   |

## Thread-Based Conversation

Previously, we used a fixed thread:

```python
CONFIG = {
    "configurable": {
        "thread_id": "thread-1"
    }
}
```

Now, a new thread ID is generated for each conversation:

```python
thread_id = uuid.uuid4()
```

This allows multiple independent conversations to exist.

```text
Thread A
├── User message
├── AI response
└── User message
    └── AI response

Thread B
├── User message
├── AI response
└── User message
    └── AI response
```

The checkpointer keeps these histories separate because they have different `thread_id` values.

## Creating a New Conversation

When **New Chat** is selected:

```text
New Chat
   ↓
Generate new UUID
   ↓
Set new thread_id
   ↓
Add thread to chat_threads
   ↓
Clear UI message_history
   ↓
Start new conversation
```

The implementation generates a UUID and stores it as the current thread ID. 

## Loading an Existing Conversation

When a user selects a previous conversation:

```text
Select Thread
     ↓
thread_id
     ↓
chatbot.get_state(config)
     ↓
Checkpointed state
     ↓
state.values["messages"]
     ↓
Display messages in UI
```

The important part is:

```python
config = {
    "configurable": {
        "thread_id": str(thread_id)
    }
}

state = chatbot.get_state(config=config)
```

The saved messages are then extracted from:

```python
state.values.get("messages", [])
```



## `thread_id` as Conversation Identity

A useful mental model:

```text
thread_id
    ↓
┌──────────────────────┐
│ Conversation History │
├──────────────────────┤
│ HumanMessage         │
│ AIMessage            │
│ HumanMessage         │
│ AIMessage             │
└──────────────────────┘
```

So:

> **`thread_id` is the identity of a particular graph execution history/conversation.**

The checkpointer uses this identity to retrieve the appropriate persisted state.

## Important Architecture Distinction

There are now **two kinds of state** in the application:

| State              | Purpose                                       |
| ------------------ | --------------------------------------------- |
| `st.session_state` | Maintains Streamlit UI state                  |
| LangGraph state    | Maintains workflow/conversation state         |
| Checkpointer       | Persists LangGraph state                      |
| `thread_id`        | Identifies which conversation state to access |

The frontend keeps `message_history` for displaying the selected conversation, while the actual LangGraph conversation is recovered from the checkpointed state. 

## Streaming + Resumable Conversations

The previous streaming functionality is still used.

The current conversation is identified by its `thread_id` and then streamed:

```text
User Input
    ↓
Current thread_id
    ↓
chatbot.stream()
    ↓
LangGraph
    ↓
Checkpointed conversation state
    ↓
LLM
    ↓
Message chunks
    ↓
Streamlit UI
```

The implementation passes the current thread ID to `chatbot.stream()` while using `stream_mode="messages"`. 

## Backend Remains Simple

The backend graph itself has not changed significantly:

```text
START
  ↓
chat_node
  ↓
END
```

The chatbot is still compiled with an `InMemorySaver` checkpointer. 

The major change is on the **application/UI side**: instead of always using one fixed thread, the application now manages multiple thread IDs.

## Main Learning

The important progression is:

```text
Single Chat
    ↓
Persistent Chat
    ↓
Streaming Chat
    ↓
Multiple Persistent Chats
    ↓
Resume / Switch Conversations
```

The key concept introduced here is:

> **A checkpointer can maintain multiple independent conversation histories by associating checkpointed state with different `thread_id` values.**

### Mental Model

**Thread ID = Conversation Identity**

**Checkpointer = Stores Conversation State**

**`get_state()` = Retrieve Conversation**

**UUID = Generate New Conversation Identity**

**`st.session_state` = Manage UI State**

**`chatbot.stream()` = Continue Conversation with Streaming**
