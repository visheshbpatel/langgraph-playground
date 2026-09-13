# 7. Conditional Workflows

A **conditional workflow** allows a graph to choose the next node based on the current state.

Unlike a sequential workflow, where the path is fixed:

```text
START → A → B → C → END
```

a conditional workflow can branch:

```text
              ┌──→ B ──→ END
START → A ────┤
              └──→ C ──→ END
```

The decision is made by a **routing function** that reads the current state and returns which node should execute next.

## New Concepts

| Concept                   | What you should understand                                                             |
| ------------------------- | -------------------------------------------------------------------------------------- |
| **Conditional workflow**  | Workflow path changes based on state/data                                              |
| `add_conditional_edges()` | Creates dynamic routing between nodes                                                  |
| **Routing function**      | Reads state and decides the next node                                                  |
| `Literal`                 | Defines the allowed routing outcomes                                                   |
| **Branching**             | One node can lead to different execution paths                                         |
| **State-based routing**   | Decisions are made using values stored in graph state                                  |
| **Dynamic control flow**  | The graph structure is defined beforehand, but the executed path can change at runtime |
| **Terminal branches**     | Different branches can independently lead to `END`                                     |
| **Structured output**     | LLM output can be constrained to a predefined schema                                   |
| `model_dump()`            | Converts a Pydantic model into a dictionary                                            |

## Conditional Routing

The basic pattern is:

```python
def check_condition(state):
    if state["value"] > 0:
        return "positive_node"
    else:
        return "negative_node"

graph.add_conditional_edges(
    "check_node",
    check_condition
)
```

Conceptually:

```text
                 ┌──→ positive_node
check_node ──────┤
                 └──→ negative_node
```

The routing function **does not perform the actual work**. Its job is only to decide **where the workflow goes next**.

## Example 1 — Quadratic Equation

The discriminant determines which branch should execute:

```text
START
  ↓
Show Equation
  ↓
Calculate Discriminant
  ↓
  ├── D > 0  ──→ Real Roots ────────→ END
  ├── D = 0  ──→ Repeated Roots ────→ END
  └── D < 0  ──→ No Real Roots ─────→ END
```

The important idea is that the same workflow can produce different execution paths depending on the state.

## Example 2 — Review Processing

The sentiment determines how a review is handled:

```text
               START
                 ↓
            find_sentiment
                 ↓
 ┌───────────────┴───────────────┐
 ↓                               ↓
Positive                       Negative
 ↓                               ↓
positive_response            run_diagnosis
 ↓                               ↓
END                         negative_response
                                ↓
                               END
                      
```

For negative reviews, the workflow performs additional processing before generating the response.

## Main Learning

> **Conditional edges turn a fixed workflow into a decision-making workflow.**

The key mental model:

> **State = Data | Node = Work | Edge = Flow | Conditional Edge = Decision**

### Important Design Rule

Use conditional routing when **the next step depends on runtime information**.

If the execution order is always the same:

```text
A → B → C
```

use normal edges.

If the next step depends on state:

```text
A → condition → B or C
```

use conditional edges.
