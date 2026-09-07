# What Is Agentic AI?

## 1. What Is Agentic AI?

**Agentic AI** refers to AI systems that can work toward a goal by making decisions, taking actions, observing results, and adapting their behaviour.

A simple mental model is:

```text
Goal
 ↓
Understand
 ↓
Plan
 ↓
Act
 ↓
Observe
 ↓
Adapt
 ↓
Repeat
```

The key idea is that the system is not limited to generating a single response. It can **decide what needs to happen next** to accomplish a goal.

> **Generative AI is a capability, whereas Agentic AI is a behaviour.**

An agentic system commonly uses an **LLM as its reasoning component**, but the complete system is more than just the LLM.

---

# 2. Key Characteristics of Agentic AI

## 2.1 Autonomy

**Autonomy** means the system can make decisions and take actions with limited step-by-step human instructions.

Instead of:

```text
Human → Step 1
Human → Step 2
Human → Step 3
```

the system can determine:

```text
Goal
 ↓
AI decides Step 1
 ↓
AI decides Step 2
 ↓
AI decides Step 3
```

Autonomy does not mean unlimited independence. The application can still define boundaries, permissions, and rules.

---

## 2.2 Goal-Oriented

An agentic system works toward a **goal**, rather than simply responding to individual instructions.

For example:

> "Find the best flight for my trip."

The system may need to:

```text
Understand requirements
       ↓
Search flights
       ↓
Compare options
       ↓
Check constraints
       ↓
Select an option
```

The goal determines what actions are relevant.

---

## 2.3 Planning

**Planning** means determining the steps required to achieve a goal.

For example:

```text
Goal: Prepare a market report

Plan:
1. Collect market data
2. Analyze the data
3. Identify important trends
4. Generate the report
```

Planning can be explicit or implicit, and the plan may change as new information becomes available.

---

## 2.4 Reasoning

**Reasoning** allows the system to determine what action makes sense based on the goal, available information, and current situation.

For example:

```text
Goal
 ↓
What information do I need?
 ↓
Which tool should I use?
 ↓
What did the tool return?
 ↓
What should I do next?
```

An LLM can provide much of this reasoning capability.

---

## 2.5 Adaptability

**Adaptability** means the system can change its approach based on new information or unexpected results.

For example:

```text
Search
 ↓
No useful result
 ↓
Change search strategy
 ↓
Search again
 ↓
Useful result
 ↓
Continue
```

A rigid workflow may fail when an expected step does not work.

An agentic system can potentially adjust its behaviour.

---

## 2.6 Context Awareness

**Context awareness** means the system considers the information available about the current task and situation when deciding what to do.

Context can include:

- User requirements
- Previous actions
- Tool results
- Current task state
- Relevant retrieved information

For example:

```text
Previous Action → Result
                  ↓
              Current Context
                  ↓
            Decide Next Action
```

This is closely related to **state and memory**, which become increasingly important as agentic systems become more complex.

---

# 3. Components of an Agentic AI System

An agentic system can be understood using five major conceptual components:

```text
                  ┌──────────────┐
                  │    Brain     │
                  │  LLM/Model   │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │ Orchestrator │
                  └──────┬───────┘
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
           Tools                  Memory
              │                     │
              └──────────┬──────────┘
                         ↓
                    Supervisor
```

These names are **conceptual roles**, not necessarily separate software components or classes.

---

## 3.1 Brain

The **Brain** is the intelligence and reasoning component of the system.

In many agentic systems, this is an **LLM**.

It can help with:

- Understanding the goal
- Reasoning about the situation
- Deciding what information is needed
- Selecting actions
- Interpreting results
- Generating the final response

```text
Goal + Context
      ↓
     LLM
      ↓
Decision
```

> **Brain = reasoning and intelligence.**

---

## 3.2 Orchestrator

The **Orchestrator** manages the flow of the system.

It coordinates things such as:

- Which component should execute next
- When a tool should be called
- How results are passed between components
- When the task should continue
- When the task should finish

Conceptually:

```text
Brain
 ↓
Orchestrator
 ↓
Tool / Memory / Other Component
 ↓
Result
 ↓
Orchestrator
 ↓
Brain
```

> **Orchestrator = manages the workflow.**

This concept becomes particularly important when building systems with **LangGraph**, where nodes, edges, state, and conditional routing can explicitly represent orchestration.

---

## 3.3 Tools

**Tools** allow the agentic system to interact with the outside world or perform operations that the LLM cannot reliably perform by itself.

Examples:

- Web search
- Calculator
- Database
- Weather API
- File operations
- Email
- External APIs

```text
Agent
 ↓
Tool
 ↓
External System
 ↓
Result
```

> **Tools = capabilities/actions.**

---

## 3.4 Memory

**Memory** allows the system to retain and use information beyond the immediate model interaction.

Memory can help an agentic system maintain things such as:

- Previous interactions
- Important information
- Task-related information
- Relevant past context

Conceptually:

```text
Previous Information
        ↓
      Memory
        ↓
     Context
        ↓
     Decision
```

Memory is important because complex tasks often require information from earlier steps.

A crucial distinction is that **context available during the current execution and persistent memory are not necessarily the same thing**.

Memory design becomes more important when the system must retain information across interactions or executions.

---

## 3.5 Supervisor

The **Supervisor** is responsible for overseeing the system and controlling whether the overall process should continue, change direction, or stop.

Conceptually:

```text
                Supervisor
                    ↓
          ┌─────────┼─────────┐
          ↓         ↓         ↓
        Agent     Tool      Other Agent
          │         │         │
          └─────────┼─────────┘
                    ↓
                Supervisor
                    ↓
              Continue / Stop
```

A supervisor can be particularly useful in systems involving multiple agents or multiple specialized components.

> **Supervisor = oversees and controls the overall process.**

---

# 4. Putting the Components Together

A simplified agentic system can be viewed as:

```text
                         Goal
                           ↓
                     ┌───────────┐
                     │   Brain   │
                     │    LLM    │
                     └─────┬─────┘
                           ↓
                    ┌──────────────┐
                    │ Orchestrator │
                    └──────┬───────┘
                           ↓
                ┌──────────┼──────────┐
                ↓          ↓          ↓
              Tools      Memory    Other Components
                │          │
                └──────────┼──────────┘
                           ↓
                       Result
                           ↓
                     Brain / LLM
                           ↓
                     Decide Again
                           ↓
                      Supervisor
                           ↓
                    Continue / Stop
```

The exact architecture can vary. Not every agentic system needs every component as a separate module.

---

# 5. Simple Mental Model

The five components can be remembered as:

| Component | Main Responsibility |
|---|---|
| **Brain** | Think and reason |
| **Orchestrator** | Coordinate the workflow |
| **Tools** | Perform actions |
| **Memory** | Retain useful information |
| **Supervisor** | Oversee and control the process |

Together:

```text
Brain        → Think
Orchestrator → Coordinate
Tools        → Act
Memory       → Remember
Supervisor   → Oversee
```

The overall agentic behaviour emerges when these capabilities work together toward a **goal**:

```text
Goal
 ↓
Think
 ↓
Plan
 ↓
Act
 ↓
Observe
 ↓
Remember Context
 ↓
Adapt
 ↓
Decide Again
 ↓
Complete Goal
```

---

# 6. Key Takeaways

### Agentic AI

> **Agentic AI is a system-level behaviour where an AI system works toward a goal by deciding, acting, observing, and adapting.**

### Autonomy

> **The system can make decisions and take actions without requiring every individual step to be specified by a human.**

### Goal-Oriented

> **The system's actions are directed toward achieving a specific goal.**

### Planning

> **The system determines the steps or strategy required to achieve the goal.**

### Reasoning

> **The system evaluates the current situation and determines what action makes sense next.**

### Adaptability

> **The system can change its approach when new information or unexpected results occur.**

### Context Awareness

> **The system uses the current task state, previous actions, results, and relevant information when making decisions.**

### Agentic System Components

```text
Brain        → Think
Orchestrator → Coordinate
Tools        → Act
Memory       → Remember
Supervisor   → Oversee
```

---

# 7. Final Mental Model

The most important mental model from this lesson is:

```text
                         GOAL
                           ↓
                    ┌─────────────┐
                    │    BRAIN    │
                    │     LLM     │
                    └──────┬──────┘
                           ↓
                    ┌─────────────┐
                    │ORCHESTRATOR │
                    └──────┬──────┘
                           ↓
                 ┌─────────┴─────────┐
                 ↓                   ↓
              TOOLS                MEMORY
                 ↓                   ↓
          External Action       Context/State
                 └─────────┬─────────┘
                           ↓
                       OBSERVE
                           ↓
                         REASON
                           ↓
                       ADAPT
                           ↓
                   DECIDE AGAIN
                           ↓
                      SUPERVISOR
                           ↓
                  CONTINUE / STOP
```

The key idea is:

> **An LLM provides much of the reasoning capability, but an agentic system is more than an LLM.**

An agentic system combines reasoning with mechanisms for **decision-making, action, observation, state/memory, orchestration, and control** to work toward a goal.

> **Agentic AI = Goal + Reasoning + Decision-Making + Actions + Observation + Adaptation**