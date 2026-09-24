# 16. Tools in LangGraph

## Key Theory

Tools allow an LLM to interact with the **outside world** and perform actions or retrieve information instead of only generating text.

In this implementation, the chatbot can decide whether to:

1. Answer directly
2. Call a tool
3. Receive the tool result
4. Continue reasoning with that result
5. Give the final response

This introduces the basic **LLM → Tool → LLM** agentic loop.

## What We Learned

| Concept           | What you should understand                                                                                |
| ----------------- | --------------------------------------------------------------------------------------------------------- |
| **Tool**          | A callable capability that allows the LLM application to perform an action or access external information |
| `@tool`           | Converts a Python function into a LangChain tool with a defined interface                                 |
| **Tool Schema**   | Describes the tool's name, inputs, and purpose so the LLM knows how to call it                            |
| `bind_tools()`    | Makes tools available to the LLM so it can request tool calls                                             |
| `ToolNode`        | LangGraph prebuilt node that executes requested tools                                                     |
| `tools_condition` | Routes execution based on whether the LLM requested a tool                                                |
| `ToolMessage`     | Message containing the result produced by a tool                                                          |
| `AIMessage`       | Can contain a tool-call request from the LLM or a normal AI response                                      |
| **Tool Calling**  | LLM decides that an external capability is needed and generates a structured tool call                    |
| **Tool Loop**     | LLM → Tool → LLM cycle used to perform actions and interpret their results                                |
| **External Tool** | Capability provided by an external service, API, search engine, database, etc.                            |
| **Custom Tool**   | A Python function defined specifically for the application                                                |

## Creating Tools

A normal Python function can be exposed as a tool using `@tool`:

```python
@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    ...
```

The function becomes a tool that the LLM can request.

The implementation contains three tools:

```text
Search Tool
    ↓
DuckDuckGoSearchRun

Calculator
    ↓
Custom Python function

Stock Price
    ↓
Alpha Vantage API
```



## Making the LLM Tool-Aware

Simply defining tools does not make the LLM use them.

The tools are provided to the model using:

```python
llm_with_tools = model.bind_tools(tools)
```

This gives the model knowledge of the available tool interfaces and allows it to generate tool-call requests. 

The important distinction is:

```text
Tools exist
     ↓
bind_tools()
     ↓
LLM knows about available tools
     ↓
LLM can request a tool call
```

## Tool Calling Flow

The chatbot now has a graph like:

```text
                 ┌──────────────┐
                 │   chat_node  │
                 │     LLM      │
                 └──────┬───────┘
                        │
                 Tool requested?
                   /          \
                 Yes            No
                  ↓              ↓
             ToolNode           END
                  │
                  ↓
             Tool result
                  │
                  └──────→ chat_node
```

This is the most important new graph pattern.

### Why the Loop Exists

The LLM may not be able to answer immediately.

For example:

```text
User:
"What is the current price of AAPL?"

        ↓

LLM
"I need the stock-price tool."

        ↓

ToolNode
Calls stock API

        ↓

Tool Result
AAPL = ...

        ↓

LLM
Interprets result

        ↓

Final Answer
```

So the graph can repeatedly move between the LLM and tools.

## `ToolNode`

LangGraph provides:

```python
tool_node = ToolNode(tools)
```

`ToolNode` is responsible for executing the tool calls requested by the LLM.

The graph registers it as a node:

```python
graph.add_node("tools", tool_node)
```



This is important because **we don't need to manually write the tool-execution logic inside our chatbot node**.

## Conditional Routing with `tools_condition`

After the LLM executes, the graph needs to determine:

> **Did the LLM request a tool, or should the workflow finish?**

This is handled by:

```python
graph.add_conditional_edges(
    "chat_node",
    tools_condition
)
```



Conceptually:

```text
chat_node
    ↓
tools_condition
    │
    ├── Tool call → tools
    │
    └── No tool call → END
```

So `tools_condition` acts as the **routing decision** after the LLM node.

## Connecting the Tool Back to the LLM

The tool node connects back to the chatbot:

```python
graph.add_edge("tools", "chat_node")
```



This creates the loop:

```text
LLM
 ↓
Tool
 ↓
LLM
 ↓
Tool
 ↓
LLM
 ↓
END
```

The LLM can therefore use multiple tools or perform multiple tool calls when required.

## Messages During Tool Calling

The message flow becomes more than just:

```text
HumanMessage → AIMessage
```

It can now involve:

```text
HumanMessage
      ↓
AIMessage
(tool call)
      ↓
ToolMessage
(tool result)
      ↓
AIMessage
(final response)
```

The frontend specifically checks for `ToolMessage` and `AIMessage` while streaming. 

## Tool Execution vs Tool Decision

This distinction is important:

| Component         | Responsibility                                    |
| ----------------- | ------------------------------------------------- |
| **LLM**           | Decides whether a tool is needed and requests it  |
| **ToolNode**      | Executes the requested tool                       |
| **Tool**          | Performs the actual external operation            |
| **Tool result**   | Provides the result back to the workflow          |
| **LLM again**     | Interprets the result and decides what to do next |
| `tools_condition` | Determines whether to go to `ToolNode` or `END`   |

This gives us a useful mental model:

> **LLM decides → Tool acts → LLM interprets**

## Streaming Tool Activity

The frontend also distinguishes between AI output and tool activity.

When a `ToolMessage` is received, the UI displays a status such as:

```text
Using `calculator` ...
```

When an `AIMessage` is received, only its content is yielded to the normal response stream. 

So the user can see that the chatbot is performing a tool action while the final response continues to stream.

## Agentic Behavior

This is an important connection to the earlier concepts.

Previously:

```text
User → LLM → Response
```

Now:

```text
User
 ↓
LLM decides
 ↓
Tool
 ↓
Observe result
 ↓
LLM decides again
 ↓
Response
```

This introduces the basic structure of an **agentic loop**.

However:

> **Having tools available does not automatically mean the system is a fully autonomous agent.**

The important behavior here is that the LLM can **dynamically decide whether a tool is needed**, and the graph provides the loop required to execute the tool and return the result to the LLM.

## Main Learning

The graph has evolved from a simple chatbot into a tool-using workflow:

```text
Simple Chatbot

START → LLM → END
```

becomes:

```text
Tool-Aware Chatbot

             ┌──────────────┐
             │     LLM      │
             └──────┬───────┘
                    │
             Need a tool?
              /         \
            Yes          No
             ↓            ↓
         ToolNode        END
             │
             ↓
            LLM
```

The key concepts introduced here are:

**Tools → `@tool` → `bind_tools()` → Tool Calling → `ToolNode` → `tools_condition` → `ToolMessage` → Conditional Routing → Tool Loop**

### Mental Model

**Tool = Capability**

**LLM = Decision Maker**

**`bind_tools()` = Give LLM access to capabilities**

**ToolNode = Tool Executor**

**`tools_condition` = Decide whether to execute a tool**

**ToolMessage = Tool Result**

**Loop = LLM → Tool → LLM**
