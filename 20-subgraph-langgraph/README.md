# Subgraphs in LangGraph

## Key Theory

A **subgraph** is a graph embedded inside another graph. It allows a complex workflow to be broken into smaller, reusable, independent workflows.

```text
Parent Graph
    ↓
  Node A
    ↓
 Subgraph
 ┌──────────────┐
 │ Node B       │
 │     ↓        │
 │ Node C       │
 └──────────────┘
    ↓
  Node D
```

### Why Use Subgraphs?

* Break large graphs into smaller components
* Keep complex logic isolated
* Make workflows easier to understand and maintain
* Reuse a workflow inside different parent graphs
* Allow different parts of an application to have their own state and logic

## What We Learned

| Concept               | What you should understand                                                     |
| --------------------- | ------------------------------------------------------------------------------ |
| **Subgraph**          | A graph used as a component inside another graph                               |
| **Parent Graph**      | The main graph that contains or calls the subgraph                             |
| **Child Graph**       | The nested graph performing a specific part of the workflow                    |
| **Shared State**      | Parent and subgraph can communicate through common state fields                |
| **State Mapping**     | When state schemas differ, data can be transformed between parent and subgraph |
| **Compiled Subgraph** | A compiled graph can be added to another graph as a node                       |
| **Modularity**        | Complex workflows can be divided into smaller graph components                 |
| **Nested Workflow**   | A workflow can contain another workflow                                        |

## Basic Structure

Conceptually:

```text
Parent Graph

START
  ↓
Node A
  ↓
┌─────────────────┐
│    Subgraph     │
│                 │
│ Node B → Node C │
└─────────────────┘
  ↓
Node D
  ↓
END
```

The parent graph does not need to manage every internal node of the subgraph.

It treats the **subgraph as a single component**, while the subgraph manages its own internal execution.

## Shared State

One important pattern is allowing the parent graph and subgraph to use a **shared state schema**.

```text
Parent State
     ↓
 Subgraph
     ↓
updates shared state
     ↓
Parent continues
```

This makes communication between the parent workflow and nested workflow straightforward.

## Why Subgraphs Matter

Without subgraphs:

```text
One Large Graph
├── Node A
├── Node B
├── Node C
├── Node D
├── Node E
├── Node F
└── Node G
```

With subgraphs:

```text
Parent Graph
├── Node A
├── Subgraph 1
│   ├── Node B
│   └── Node C
├── Subgraph 2
│   ├── Node D
│   └── Node E
└── Node F
```

This gives us **hierarchical workflow design**.

### Mental Model

**Parent Graph = Overall Workflow**

**Subgraph = Self-contained Workflow**

**Node = Unit of Work**

**Shared State = Communication**

**Subgraph = Modularize Complex Graphs**
