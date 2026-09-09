# Lesson 4 — LLM Workflows and LangGraph Fundamentals

## 1. LLM Workflow

An **LLM workflow** is a structured sequence of steps where one or more LLM calls, tools, or processing components work together to accomplish a task.

Instead of asking a single LLM call to perform an entire complex task:

```text
User
 ↓
LLM
 ↓
Final Answer
```

we can break the task into smaller steps:

```text
User
 ↓
Step 1
 ↓
Step 2
 ↓
Step 3
 ↓
Final Result
```

This provides better **control, predictability, debugging, validation, and flexibility**.

### Common LLM Workflow Patterns

| Pattern              | Main Idea                                   |
| -------------------- | ------------------------------------------- |
| Prompt Chaining      | Sequentially execute dependent steps        |
| Routing              | Choose which path should handle the request |
| Parallelization      | Execute independent tasks concurrently      |
| Orchestrator–Workers | Dynamically divide work among workers       |
| Evaluator–Optimizer  | Generate, evaluate, and improve iteratively |

---

## 1.1 Prompt Chaining

**Prompt Chaining** means connecting multiple LLM steps where the output of one step becomes the input to the next step.

```text
Input
  ↓
Step 1
  ↓
Step 2
  ↓
Step 3
  ↓
Output
```

### Example

Creating a technical article:

```text
Generate Outline
      ↓
Write Article
      ↓
Review Article
      ↓
Improve Article
```

Each step depends on the result of the previous step.

### Mental Model

> **Do A → use its result → do B → use its result → do C**

### When to use

Use prompt chaining when a task naturally consists of **dependent sequential steps**.

---

## 1.2 Routing

**Routing** means deciding which path should handle a request based on the input or current state.

```text
             ┌──→ Technical
             │
Input → Router ──→ Coding
             │
             └──→ General
```

For example:

```text
User Question
      ↓
   Router
   ↙   ↓   ↘
DBMS Python LangGraph
```

The router determines which specialized path should execute.

### Mental Model

> **"Where should this request go?"**

### Important distinction

Prompt chaining follows a predefined sequence.

Routing **selects a path**.

### LangGraph connection

Routing is commonly represented using **conditional edges**.

---

## 1.3 Parallelization

**Parallelization** means executing independent tasks at the same time rather than waiting for each task sequentially.

```text
             ┌──→ Task A ──┐
             │             │
Input ───────┼──→ Task B ──┼──→ Combine
             │             │
             └──→ Task C ──┘
```

### Example

Analyzing a product:

```text
Product
   ↓
   ├──→ Analyze Price
   ├──→ Analyze Reviews
   └──→ Analyze Features
              ↓
         Combine Results
```

If these analyses are independent, there is no reason for one to wait for another.

### Mental Model

> **"These tasks are independent, so execute them together."**

### LangGraph connection

Parallel execution becomes especially important when multiple nodes update the same **state**.

This is where **Reducers** become important.

---

## 1.4 Orchestrator–Workers

In an **Orchestrator–Workers** pattern, a central orchestrator determines what work needs to be performed and delegates that work to workers.

```text
                ┌──→ Worker 1
                │
Input → Orchestrator ─→ Worker 2
                │
                └──→ Worker 3
```

For example, for a research task:

```text
                Orchestrator
                     ↓
        ┌────────────┼────────────┐
        ↓            ↓            ↓
   Research DBMS  Research AI  Research Security
        ↓            ↓            ↓
        └────────────┼────────────┘
                     ↓
                 Final Report
```

The important part is that the orchestrator can determine **what work should be done** and **which workers should perform it**.

### Difference from Parallelization

Parallelization:

```text
Always run A + B + C
```

Orchestrator–Workers:

```text
Orchestrator decides:

"What work is needed?"
"How should it be divided?"
"Which worker should handle it?"
```

### Mental Model

> **"What work needs to happen, and who should do it?"**

---

## 1.5 Evaluator–Optimizer

The **Evaluator–Optimizer** pattern introduces feedback into the workflow.

A system generates an output, evaluates it, and improves it if necessary.

```text
Generate
   ↓
Evaluate
   ↓
Good enough?
  ↙     ↘
 No      Yes
 ↓        ↓
Improve  Output
 ↓
 └────→ Evaluate
```

### Example

```text
Generate Answer
      ↓
Evaluate Answer
      ↓
Is it accurate?
   ↙       ↘
 No         Yes
 ↓           ↓
Improve    Final Answer
 ↓
 └────────→ Evaluate
```

Unlike simple chaining, this workflow can **loop**.

### Mental Model

> **Generate → Evaluate → Improve → Evaluate → Finish**

### LangGraph connection

This pattern maps naturally to **cycles/loops in a graph**.

---

# 2. Graphs, Nodes, and Edges

LangGraph represents workflows using a **graph**.

A graph consists primarily of:

```text
Graph
 ├── Nodes
 └── Edges
```

---

## 2.1 Graph

A **graph** represents the overall workflow and defines how different pieces of work are connected.

For example:

```text
START
  ↓
Generate
  ↓
Validate
  ↓
Improve
  ↓
END
```

The graph describes the **structure and execution flow** of the application.

### Mental Model

> **The graph is the blueprint of the workflow.**

---

## 2.2 Nodes

A **node** represents a unit of work.

A node can:

* Call an LLM
* Call a tool
* Process data
* Validate information
* Perform business logic
* Make a decision
* Transform state

Example:

```text
START
  ↓
Generate Answer    ← Node
  ↓
Validate Answer    ← Node
  ↓
END
```

A node generally:

```text
Read State
    ↓
Perform Work
    ↓
Update State
```

### Mental Model

> **Node = Work**

---

## 2.3 Edges

An **edge** determines what happens after a node finishes.

```text
Node A
  ↓
Node B
```

The edge represents the transition from one node to another.

Example:

```text
Generate
   ↓
Validate
   ↓
END
```

There are also **conditional edges**, where the next node depends on the current state.

```text
          ┌──→ Improve
Validate ─┤
          └──→ END
```

### Mental Model

> **Edge = Movement / Transition**

---

## Graph Mental Model

Think of LangGraph as:

```text
           ┌──────────────┐
           │     Graph    │
           │              │
           │  Node → Node │
           │    ↓         │
           │  Node → Node │
           └──────────────┘
```

Or more simply:

> **Graph = Structure**
> **Node = Work**
> **Edge = Control Flow**

---

# 3. State

**State** is the shared information that represents the current condition of the workflow.

It contains the information that nodes need to read and update while the graph executes.

For example:

```text
State
├── user_input
├── messages
├── tool_results
├── intermediate_data
└── final_answer
```

A node can read information from the state:

```text
State
  ↓
Node
```

and produce an update:

```text
Node
  ↓
State Update
```

---

## Why do we need State?

Consider a multi-step workflow:

```text
User Input
    ↓
Generate
    ↓
Validate
    ↓
Improve
```

The validation node needs to know what the generation node produced.

Instead of manually passing every piece of information between functions, the graph maintains shared state.

```text
             State
          ↙    ↓    ↘
      Node A  Node B  Node C
```

### Mental Model

Think of state as a **shared workspace** for the graph.

Each node:

1. Reads the information it needs.
2. Performs its work.
3. Produces updates to the state.

---

## State is not the same as Memory

These concepts are related but different.

### State

Information available to the workflow during execution.

```text
Current task
Current messages
Tool results
Intermediate results
```

### Memory

Information intentionally retained across executions or interactions.

```text
User preferences
Previous conversations
Long-term information
```

So:

> **State = what the workflow currently knows**

> **Memory = what the system intentionally remembers**

---

# 4. Reducers

Reducers become important when **multiple nodes update the same state field**.

Suppose we have parallel nodes:

```text
             ┌──→ Node A ──→ Result A
             │
Input ───────┼──→ Node B ──→ Result B
             │
             └──→ Node C ──→ Result C
```

All three nodes may want to update the same state field.

The system needs to know:

> **"How should these updates be combined?"**

That is the job of a **Reducer**.

---

## Reducer Mental Model

A reducer defines how a new value should be combined with the existing value.

Conceptually:

```text
Existing State
      +
Node Update
      ↓
   Reducer
      ↓
Updated State
```

For multiple updates:

```text
Existing State
      +
Update A
      +
Update B
      +
Update C
      ↓
   Reducer
      ↓
Final State
```

---

## Example

Suppose the state contains:

```text
results = []
```

Three parallel nodes produce:

```text
Node A → "Result A"
Node B → "Result B"
Node C → "Result C"
```

A reducer could combine them as:

```text
["Result A", "Result B", "Result C"]
```

Instead of one update overwriting another.

### Why Reducers Matter

Reducers define the **state update semantics**.

They become particularly important for:

* Parallel execution
* Multiple nodes updating the same field
* Accumulating messages
* Combining results
* Maintaining collections of information

### Important distinction

A **node decides what update it wants to produce**.

A **reducer decides how that update is applied to the state**.

---

# 5. LangGraph Execution Model

Understanding the execution model is important because LangGraph isn't simply:

```text
Call Node A
↓
Call Node B
↓
Call Node C
```

LangGraph uses a graph-based execution model involving **state updates, message passing, node activation, and super-steps**.

The high-level lifecycle is:

```text
Graph Definition
      ↓
Compilation
      ↓
Invocation
      ↓
Super-Step
      ↓
Node Activation
      ↓
State Updates
      ↓
Next Super-Step
      ↓
...
      ↓
Halting
```

---

# 5.1 Graph Definition

First, we define the graph.

We specify:

* State
* Nodes
* Edges
* Entry point
* Routing logic
* End conditions

Conceptually:

```text
State
 ↓
Nodes
 ↓
Edges
 ↓
Graph
```

Example:

```text
START
  ↓
Generate
  ↓
Validate
  ↓
END
```

At this stage, we are describing **what the workflow looks like**.

---

# 5.2 Compilation

After defining the graph, it is **compiled**.

Conceptually:

```text
Graph Definition
      ↓
   Compile
      ↓
Executable Graph
```

Compilation prepares the graph for execution and validates the graph structure.

The important distinction is:

> **Definition describes the graph. Compilation prepares it for execution.**

Compilation does not mean the entire workflow has already run.

---

# 5.3 Invocation

Once compiled, the graph can be executed by providing an initial input/state.

Conceptually:

```text
Input State
     ↓
Compiled Graph
     ↓
Execution
```

For example:

```text
{
    user_input: "Explain DBMS"
}
```

This initializes the execution.

### Mental Model

> **Invocation = "Run the graph with this input."**

---

# 5.4 Super-Step Begin

A **super-step** is a logical phase of graph execution.

At the beginning of a super-step, LangGraph determines which nodes are active based on the current execution state and messages/updates available to them.

Conceptually:

```text
Super-Step
    ↓
Identify Active Nodes
    ↓
Execute Active Nodes
    ↓
Collect Updates
    ↓
Apply Updates
    ↓
Next Super-Step
```

This model is particularly useful for understanding **parallel execution**.

---

# 5.5 Message Passing and Node Activation

Nodes communicate indirectly through **state updates/messages**.

Conceptually:

```text
Node A
  ↓
Update State
  ↓
State / Message
  ↓
Node B becomes eligible
  ↓
Node B executes
```

For parallel execution:

```text
              ┌──→ Node A
              │
State ────────┼──→ Node B
              │
              └──→ Node C
```

Multiple nodes can become active in the same execution phase.

After they execute, their updates are collected and applied to the state.

This is where reducers can become important:

```text
Node A ──→ Update A ──┐
                      │
Node B ──→ Update B ──┼──→ Reducer → State
                      │
Node C ──→ Update C ──┘
```

---

# 5.6 Halting Conditions

The graph must eventually determine when execution is complete.

Execution can halt when:

* The graph reaches `END`
* There are no more active nodes/tasks
* A configured stopping condition is reached
* Execution is interrupted or otherwise stopped

Conceptually:

```text
Execute
   ↓
Any work remaining?
  ↙        ↘
Yes         No
 ↓           ↓
Continue    Stop
```

For a simple workflow:

```text
START
  ↓
Generate
  ↓
Validate
  ↓
END
```

Once `END` is reached, execution finishes.

For a loop:

```text
Generate
   ↓
Evaluate
   ↓
Good?
 ↙    ↘
No    Yes
↓      ↓
Improve END
  │
  └──→ Evaluate
```

The graph continues until the routing logic reaches the stopping condition.

---

# Complete Mental Model

The concepts in this lesson connect together:

```text
                LLM WORKFLOW
                     │
                     ↓
                  GRAPH
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
        NODES                  EDGES
       "Work"             "Movement"
          │
          ↓
        STATE
   "Shared Information"
          │
          ↓
       REDUCERS
 "How updates are combined"
          │
          ↓
    EXECUTION MODEL
          │
          ├── Graph Definition
          ├── Compilation
          ├── Invocation
          ├── Super-Steps
          ├── Node Activation
          ├── State Updates
          └── Halting
```

## Workflow Pattern → LangGraph Concept

| Workflow Pattern             | Graph Representation           |
| ---------------------------- | ------------------------------ |
| Prompt Chaining              | Sequential nodes + edges       |
| Routing                      | Conditional edges              |
| Parallelization              | Multiple active nodes          |
| Orchestrator–Workers         | Dynamic task/routing structure |
| Evaluator–Optimizer          | Cycles/loops                   |
| Shared information           | State                          |
| Combining concurrent updates | Reducers                       |
| Overall execution            | Graph runtime                  |

---

# Core Mental Models

### LLM Workflow

> **Break a complex task into coordinated steps.**

### Graph

> **The structure of the workflow.**

### Node

> **A unit of work.**

### Edge

> **A transition between units of work.**

### State

> **The information the workflow currently carries.**

### Reducer

> **The rule that determines how state updates are combined.**

### Execution

> **Activate nodes → produce updates → apply updates → activate next nodes → repeat until the graph halts.**

---

# The Most Important Connection

The real reason these concepts matter is that they solve the limitations we discussed in **Lesson 3**.

In complex LLM applications:

```text
Control Flow
     ↓
Graphs + Edges + Conditional Routing

Shared Information
     ↓
State

Concurrent Updates
     ↓
Reducers

Iterative Behaviour
     ↓
Loops / Cycles

Complex Execution
     ↓
LangGraph Runtime
```

So LangGraph is not just about learning APIs such as `StateGraph`, nodes, and edges.

The deeper idea is:

> **LangGraph gives us a structured way to represent, control, and execute stateful LLM workflows.**
