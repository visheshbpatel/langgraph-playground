# Observability with LangSmith

## Key Theory

**Observability** means being able to inspect what happened inside an AI application while it was running.

For a LangGraph application, observability helps us understand:

* Which nodes executed
* What inputs and outputs were produced
* How long execution took
* What the LLM generated
* How different runs relate to each other
* How a particular conversation or request behaved

**LangSmith** provides tracing and observability for LangChain and LangGraph applications.

## What We Learned

| Concept                | What you should understand                                                   |
| ---------------------- | ---------------------------------------------------------------------------- |
| **Observability**      | Ability to inspect and understand application execution                      |
| **LangSmith**          | Platform for tracing, debugging, evaluating, and monitoring LLM applications |
| **Tracing**            | Recording the execution of an application as a trace/run                     |
| **Run**                | A recorded execution of a component or operation                             |
| **Trace**              | Execution history showing how a request flowed through the application       |
| `LANGCHAIN_TRACING_V2` | Enables LangSmith tracing                                                    |
| `LANGCHAIN_ENDPOINT`   | Specifies the LangSmith API endpoint                                         |
| `LANGCHAIN_API_KEY`    | Authentication key used to send traces to LangSmith                          |
| `LANGCHAIN_PROJECT`    | Groups traces under a specific LangSmith project                             |
| `run_name`             | Gives a meaningful name to a particular execution                            |
| **Debugging**          | Use traces to understand unexpected behavior and failures                    |
| **Monitoring**         | Observe application behavior over time                                       |

## LangSmith Configuration

Add the following to `.env`:

```env
# LangSmith

LANGCHAIN_TRACING_V2=true

LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"

LANGCHAIN_API_KEY=""

LANGCHAIN_PROJECT="chatbot-project-langgraph"
```

The API key should contain your actual LangSmith API key.

Once tracing is enabled, LangChain/LangGraph execution can be sent to LangSmith for inspection.

## Observability Flow

```text
User Request
     ↓
Streamlit
     ↓
LangGraph
     ↓
Nodes / LLM / Tools
     ↓
Execution Trace
     ↓
LangSmith
     ↓
Inspect / Debug / Monitor
```

The important idea is that **LangSmith observes the execution; it does not replace the LangGraph workflow.**

## `run_name`

The frontend adds:

```python
CONFIG = {
    "configurable": {
        "thread_id": str(st.session_state["thread_id"])
    },
    "run_name": "chat_turn"
}
```

This gives the execution a meaningful name such as `chat_turn`, making traces easier to identify and understand in LangSmith. 

## Persistence + Observability

The application now has two different concerns:

```text
             LangGraph Application
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
     Persistence          Observability
          ↓                   ↓
    SqliteSaver           LangSmith
          ↓                   ↓
 Save/restore state     Inspect execution
```

The backend now uses `SqliteSaver`, which stores LangGraph checkpoints in SQLite. 

LangSmith, on the other hand, is concerned with **observing and understanding execution**.

### Important Distinction

| Persistence                         | Observability                                 |
| ----------------------------------- | --------------------------------------------- |
| Saves application state             | Records application execution                 |
| Used to resume conversations        | Used to inspect/debug execution               |
| Checkpointer                        | LangSmith tracing                             |
| `SqliteSaver`                       | LangSmith                                     |
| Answers **“What state do I have?”** | Answers **“What happened during execution?”** |

## Persistent Threads from SQLite

The backend also introduces:

```python
def retrieve_all_threads():
    all_threads = {}

    for checkpoint in checkpointer.list(None):
        thread_id = checkpoint.config['configurable']['thread_id']
        all_threads[thread_id] = None

    return list(all_threads.keys())
```

This retrieves thread IDs from the persisted checkpoints instead of relying only on Streamlit's temporary session state. 

The frontend uses this when initializing its conversation list:

```python
st.session_state["chat_threads"] = retrieve_all_threads()
```



This means conversations can be recovered from the SQLite-backed persistence layer even when they are not currently present in the Streamlit session state.

## Overall Architecture

```text
                    User
                     ↓
                Streamlit UI
                     ↓
                 thread_id
                     ↓
              chatbot.stream()
                     ↓
              ┌──────────────┐
              │  LangGraph   │
              │              │
              │   chat_node  │
              └──────┬───────┘
                     ↓
                    LLM
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
     SqliteSaver             LangSmith
     Persistence            Observability
          ↓                     ↓
  Conversation State       Execution Traces
```

## Main Learning

The application has now moved from a simple in-memory chatbot toward a more realistic architecture:

```text
InMemorySaver
      ↓
Persistent SQLite storage
      ↓
Multiple resumable conversations
      ↓
Streaming responses
      ↓
LangSmith observability
```

The key distinction to remember:

> **Persistence tells us what state was saved.**

> **Observability tells us what happened during execution.**

### Mental Model

**LangGraph = Orchestration**

**Checkpointer = Persistence**

**SQLite = Durable State Storage**

**LangSmith = Observability**

**Trace = Execution Record**

**Run = Individual Recorded Execution**

**`run_name` = Meaningful Name for a Run**
