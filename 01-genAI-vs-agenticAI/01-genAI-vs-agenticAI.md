# Generative AI vs Agentic AI

## 1. Generative AI

**Generative AI** is the capability of an AI system to generate new content such as:

- Text
- Code
- Images
- Audio
- Video

For an LLM application:

```text
User → LLM → Generated Response
```

An LLM can generate and reason over a request, but it does not automatically have access to external systems or the ability to perform actions.

> **Generative AI is a capability.**

---

## 2. Agentic AI

**Agentic AI** describes how an AI system behaves when working toward a goal.

An agentic system can:

1. Understand a goal.
2. Decide what to do.
3. Take an action.
4. Observe the result.
5. Decide what to do next.
6. Repeat until the goal is completed.

```text
Goal
 ↓
Decide
 ↓
Act
 ↓
Observe
 ↓
Decide Again
 ↓
...
```

> **Agentic AI is a behaviour.**

An LLM can be the reasoning component inside an agent, but an LLM by itself is not necessarily an agent.

---

## 3. Generative AI vs Agentic AI

| Generative AI | Agentic AI |
|---|---|
| Capability | Behaviour |
| Generates content | Pursues a goal |
| Can answer a request | Can decide what to do next |
| Does not require tools | Can use tools |
| Does not require a decision loop | Commonly uses a decision/action loop |

The two concepts are complementary:

```text
Generative AI
     ↓
Generation + Reasoning
     ↓
Can be used inside
     ↓
Agentic System
```

---

# 4. AI Chatbot Architectures

AI chatbots can be understood by the capabilities added around an LLM.

```text
Basic LLM
   ↓
RAG
   ↓
Tool-Augmented System
   ↓
Agentic System
```

These are not necessarily separate systems. A more advanced system can combine the previous capabilities.

---

## 4.1 Basic LLM Chatbot

### Architecture

```text
User → LLM → Response
```

### What It Solves

Useful for:

- General questions
- Explanations
- Content generation
- Conversation
- Rewriting

### Limitation

The LLM does not automatically have access to application-specific or real-time information.

---

## 4.2 RAG-Based Chatbot

**RAG = Retrieval-Augmented Generation**

RAG retrieves relevant information from an external knowledge source and provides it to the LLM.

```text
User Query
    ↓
Retrieve Relevant Information
    ↓
LLM + Retrieved Context
    ↓
Answer
```

### What It Solves

RAG is useful for answering questions about:

- Private documents
- Company data
- Knowledge bases
- Domain-specific information

### Mental Model

> **RAG gives the model information.**

RAG is mainly about **retrieving knowledge**, not performing actions.

---

## 4.3 Tool-Augmented Chatbot

A **tool** gives an AI application an external capability.

Examples:

- Calculator
- Web search
- Weather API
- Database
- Email service
- Calendar

```text
User
 ↓
LLM
 ↓
Tool
 ↓
Tool Result
 ↓
LLM
 ↓
Answer
```

### Mental Model

> **RAG gives information; tools provide capabilities/actions.**

For example:

```text
"What is the weather?"
        ↓
   Weather Tool
        ↓
Current Weather
```

## 4.4 Agentic AI Chatbot

An **agentic AI chatbot** uses an LLM as a reasoning component to dynamically decide what actions to take in order to achieve a goal.

Unlike a fixed workflow, the next step is not always predetermined. The system can choose a tool, use its result, and decide what to do next.

### Architecture

```text
User Goal
    ↓
LLM / Agent
    ↓
Decide Next Action
    ↓
Tool / External System
    ↓
Observe Result
    ↓
LLM / Agent
    ↓
Decide Next Action
    ↓
...
    ↓
Final Answer
```

### What It Solves

Agentic systems are useful when a task requires:

- Multiple steps
- Dynamic decision-making
- Multiple tools
- Adapting based on tool results
- Completing a goal rather than simply answering a question

### Example

Suppose the user asks:

> Find the best flight for my trip and compare the available options.

An agentic system might:

```text
Goal
 ↓
Search Flights
 ↓
Observe Results
 ↓
Filter Relevant Flights
 ↓
Compare Prices and Times
 ↓
Decide More Information Is Needed
 ↓
Search Again
 ↓
Observe Results
 ↓
Final Recommendation
```

The important characteristic is that the agent can **decide what to do next based on the current state and observations**.

### Mental Model

> **An agent pursues a goal by reasoning, acting, observing, and adapting.**

```text
Goal
 ↓
Reason
 ↓
Act
 ↓
Observe
 ↓
Reason Again
 ↓
Act Again
 ↓
...
 ↓
Goal Completed
```

An agentic chatbot can combine **LLMs, RAG, tools, memory, and other components** depending on the application's requirements.

---

# 5. Tool Calling vs Agentic AI

Using a tool does **not automatically mean the system is agentic**.

### Fixed Workflow

```text
Search
 ↓
Calculate
 ↓
Answer
```

If the application always follows this predefined sequence, it is better understood as a **tool-augmented workflow**.

### Dynamic Workflow

```text
Goal
 ↓
LLM decides what to do
 ↓
Tool
 ↓
Observe result
 ↓
LLM decides what to do next
 ↓
Another Tool
 ↓
...
```

This demonstrates stronger **agentic behaviour** because the system dynamically decides its next action based on what happens.

> **Tool calling is a capability. Agentic behaviour is the dynamic decision-making around those capabilities.**

---

# 6. Example: Bitcoin Price

Suppose the goal is:

> Find the latest Bitcoin price, compare it with yesterday's price, calculate the percentage change, and determine whether it increased or decreased.

A fixed workflow could be:

```text
Search Current Price
        ↓
Search Yesterday's Price
        ↓
Calculator
        ↓
Answer
```

This uses tools, but the sequence is predetermined.

An agentic system could instead:

```text
Goal
 ↓
Decide how to get current price
 ↓
Search
 ↓
Observe
 ↓
Decide how to get yesterday's price
 ↓
Search
 ↓
Observe
 ↓
Decide calculation is needed
 ↓
Calculator
 ↓
Observe
 ↓
Decide whether goal is complete
 ↓
Final Answer
```

The important difference is **not simply that tools are being used**.

The important difference is whether the system can **dynamically decide and adapt what to do next**.

---

# 7. Core Mental Models

### Generative AI

> **"I can generate."**

```text
Input → LLM → Output
```

### RAG

> **"I can generate using external information."**

```text
Query → Retrieve → Context → LLM → Answer
```

### Tools

> **"I can perform an external operation."**

```text
LLM → Tool → External System → Result
```

### Agentic AI

> **"I can decide what to do, take action, observe the result, and decide what to do next."**

```text
Goal → Decide → Act → Observe → Decide Again
```

---

# 8. Overall Understanding

The concepts are best understood as **composable capabilities**:

```text
                    LLM
              Generate + Reason
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
         RAG                Tools
          ↓                   ↓
 External Knowledge    External Actions
          │                   │
          └─────────┬─────────┘
                    ↓
             Agentic Behaviour
                    ↓
          Decide → Act → Observe
```

## Key Distinction

> **Generative AI is a capability, whereas Agentic AI is a behaviour.**

And:

> **An agent is not simply an LLM with tools. Agentic behaviour comes from dynamically deciding, acting, observing, and adapting toward a goal.**