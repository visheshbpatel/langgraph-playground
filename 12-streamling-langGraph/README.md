# 12. Streaming in LangGraph


**Streaming** means sending the output progressively as it is produced instead of waiting for the complete response.

In this implementation, LangGraph streams the LLM's message chunks and Streamlit displays them incrementally using `st.write_stream()`.

### What We Learned

| Concept                  | What you should understand                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| **Streaming**            | Sends output progressively instead of waiting for the complete result                       |
| **Why Streaming**        | Improves responsiveness and user experience, especially for LLM responses                   |
| **Generator**            | Python mechanism that produces values one at a time instead of returning everything at once |
| `yield`                  | Produces the next value from a generator while preserving its execution state               |
| `chatbot.stream()`       | Executes the LangGraph workflow in streaming mode                                           |
| `stream_mode='messages'` | Streams LLM message chunks produced during graph execution                                  |
| `message_chunk`          | A partial piece of the LLM response received during streaming                               |
| `st.write_stream()`      | Streamlit utility that displays streamed content progressively                              |
| **Streaming Pipeline**   | LangGraph produces chunks → Streamlit consumes chunks → UI displays them                    |

## How Streaming Works

Without streaming:

```text
User Input
    ↓
LangGraph
    ↓
LLM generates complete response
    ↓
Complete response returned
    ↓
UI displays response
```

With streaming:

```text
User Input
    ↓
LangGraph
    ↓
LLM
    ↓
Chunk 1 → UI
Chunk 2 → UI
Chunk 3 → UI
Chunk 4 → UI
...
```

The important difference is **when the user receives the output**.

## Streaming in the Implementation

The frontend uses:

```python
chatbot.stream(
    {'messages': [HumanMessage(content=user_input)]},
    config=CONFIG,
    stream_mode='messages'
)
```

Instead of:

```python
chatbot.invoke(...)
```

`invoke()` waits for the workflow result, while `stream()` allows results to be consumed progressively.

The streamed chunks are then passed to:

```python
st.write_stream(...)
```

So the frontend can display the response as it arrives. 

## Generators in Python

A **generator** is an object that produces values one at a time.

Instead of:

```text
return [A, B, C, D]
```

a generator conceptually does:

```text
yield A
yield B
yield C
yield D
```

The consumer can process each value as it becomes available.

This makes generators a natural fit for streaming because the producer does not need to create the entire result before the consumer starts receiving data.

### Mental Model

```text
Generator
    ↓
produces one value
    ↓
consumer processes it
    ↓
generator resumes
    ↓
produces next value
    ↓
...
```

## LangGraph + Streaming

The underlying graph itself is still the same:

```text
START → chat_node → END
```

Streaming **does not change the graph's control flow**.

It changes **how execution results are delivered to the caller**.

The backend still defines the chatbot as a normal LangGraph workflow with a `chat_node` and edges from `START` to `END`. 

Therefore:

> **Graph structure controls what executes; streaming controls how execution output is delivered.**



## Main Learning

Streaming is not a new workflow pattern like parallelism or conditional routing.

It is an **execution/output mechanism** that allows results to be consumed progressively.

The key concepts introduced here are:

**Streaming → Generators → `stream()` → `stream_mode` → Message Chunks → `st.write_stream()`**

### Mental Model

**`invoke()` = Give me the result when you're done.**

**`stream()` = Give me the results as they become available.**
