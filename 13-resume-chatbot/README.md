# 13. Resume Chatbot

## Key Theory

This lesson extends the previous **streaming chatbot** by allowing multiple conversations to be created, stored, and resumed.

The main idea is:

> **Each conversation gets its own `thread_id`, and LangGraph's checkpointer stores the state associated with that thread.**

The UI can then switch between threads and load the corresponding conversation state.

## New Concepts

| Concept                 | What you should understand                                               |
| ----------------------- | ------------------------------------------------------------------------ |
| **Conversation Thread** | A separate conversation identified by a unique `thread_id`               |
| **Unique Thread ID**    | Prevents different conversations from sharing the same LangGraph state   |
| `uuid.uuid4()`          | Generates a unique identifier for each new conversation                  |
| `Generate_thread_id()`  | Creates a new ID for a conversation                                      |
| `chat_threads`          | Streamlit-side collection used to keep track of available conversations  |
| `reset_chat()`          | Creates a new conversation and clears the current UI history             |
| `add_thread()`          | Adds a conversation ID to the list of available threads                  |
| `load_conversation()`   | Retrieves the saved LangGraph state for a selected thread                |
| `get_state()`           | Reads the current checkpointed state for a specific thread               |
| `state.values`          | Contains the state data stored in the retrieved checkpoint               |
| **Resume Chat**         | Selecting an existing thread restores its previous messages              |
| **Thread Switching**    | Changing `thread_id` changes which conversation state LangGraph accesses |

## Thread-Based Persistence

Previously, the chatbot used a fixed thread:

```text
thread-1
```

Now every conversation gets its own ID:

```text
Conversation A → thread_id = UUID-A
Conversation B → thread_id = UUID-B
Conversation C → thread_id = UUID-C
```

LangGraph therefore maintains separate state for each conversation.

```text
                Checkpointer
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    Thread A      Thread B      Thread C
     messages      messages      messages
```

The backend graph itself remains essentially the same; the important change is how the frontend manages and selects the `thread_id`. 

## Creating a New Conversation

A new conversation generates a unique ID:

```python
thread_id = uuid.uuid4()
```

The application stores that ID in Streamlit state and clears the current UI message history.

```text
New Chat
   ↓
Generate UUID
   ↓
Create new thread
   ↓
Clear UI history
   ↓
Start new conversation
```

This is implemented through `Generate_thread_id()` and `reset_chat()`. 

## Resuming a Conversation

When the user selects an existing conversation:

```text
Select Thread
     ↓
Get thread_id
     ↓
chatbot.get_state(config)
     ↓
Retrieve checkpointed state
     ↓
Extract messages
     ↓
Display conversation
```

The important part is:

```python
config = {
    'configurable': {
        'thread_id': str(thread_id)
    }
}

state = chatbot.get_state(config=config)
```

The saved messages are then extracted from:

```python
state.values.get('messages', [])
```

This allows the UI to reconstruct the selected conversation. 

## Thread Switching

The sidebar maintains a list of conversation IDs.

When the user clicks a thread:

```text
Thread A selected
      ↓
thread_id = A
      ↓
get_state(A)
      ↓
load messages
      ↓
display conversation A
```

Selecting Thread B performs the same process with B.

The **thread ID acts as the key that tells the checkpointer which conversation state to retrieve.**

## Streamlit State vs LangGraph State

This lesson makes the distinction even more important:

| State                 | Purpose                                                    |
| --------------------- | ---------------------------------------------------------- |
| `st.session_state`    | Manages UI/application state inside the Streamlit session  |
| LangGraph `ChatState` | Stores the workflow's conversation state                   |
| Checkpointer          | Persists LangGraph checkpoints                             |
| `thread_id`           | Identifies which conversation/checkpoint history to access |

So:

```text
Streamlit
   │
   ├── chat_threads
   ├── current thread_id
   └── message_history
          │
          ↓
      LangGraph
          │
      thread_id
          │
          ↓
     Checkpointer
          │
          ↓
   Saved conversation state
```

The frontend maintains its own `message_history` for displaying the UI, while LangGraph remains responsible for the persisted workflow state.

##  12 →  13

|  12 — Streaming           |  13 — Resume Chatbot                    |
| ------------------------- | --------------------------------------- |
| `chatbot.stream()`        | `chatbot.get_state()`                   |
| Stream response chunks    | Retrieve saved conversation state       |
| `stream_mode='messages'`  | `thread_id`-based state access          |
| `st.write_stream()`       | Load and display previous messages      |
| Focus: progressive output | Focus: multiple/resumable conversations |
| One conversation flow     | Multiple conversation threads           |

## Overall Architecture

```text
User
 ↓
Streamlit UI
 ↓
Select / Create Thread
 ↓
thread_id
 ↓
LangGraph
 ↓
Checkpointer
 ↓
Conversation State
 ↓
Chat Node
 ↓
LLM
 ↓
Stream Response
 ↓
Streamlit UI
```

## Main Learning

The key addition is **thread-based conversation management**.

A single LangGraph chatbot can maintain multiple independent conversation histories by associating each execution with a different `thread_id`.

### Mental Model

**Thread ID = Which conversation?**

**Checkpointer = Where the conversation state is persisted**

**`get_state()` = Retrieve that conversation**

**`uuid4()` = Create a new conversation identity**

**Resume = Select thread → retrieve state → continue using the same thread**
