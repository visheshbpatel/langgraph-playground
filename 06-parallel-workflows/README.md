# 6. Parallel Workflows

A **parallel workflow** executes multiple independent tasks at the same time instead of running them one after another.

```text
              ┌──→ Node A ──┐
START ────────┼──→ Node B ──┼──→ Final Node ──→ END
              └──→ Node C ──┘
```

The main idea is **Fan-out → Parallel Execution → Fan-in**:

* **Fan-out** — one point starts multiple independent branches.
* **Parallel execution** — independent nodes process the same state concurrently.
* **Fan-in** — a later node waits for all required branches and combines their results.

## New Concepts

| Concept                    | What you should understand                                             |
| -------------------------- | ---------------------------------------------------------------------- |
| **Parallel workflow**      | Independent tasks can execute concurrently                             |
| **Fan-out**                | One node/entry point branches into multiple paths                      |
| **Fan-in**                 | Multiple branches converge into a common next node                     |
| **Parallel nodes**         | Nodes connected from the same predecessor can run independently        |
| **Shared state**           | Parallel nodes can read the same input state                           |
| **Reducer**                | Defines how multiple node updates to the same state field are combined |
| `Annotated`                | Used to attach a reducer/metadata to a state field                     |
| `operator.add`             | Combines list updates by addition/concatenation                        |
| **Synchronization**        | A downstream node executes after all required parallel branches finish |
| `with_structured_output()` | Makes an LLM return data matching a defined schema                     |
| `Pydantic` schema          | Defines the expected structure and validation of structured LLM output |

## Reducers

When multiple parallel nodes update the **same state key**, LangGraph needs to know how those updates should be combined.

Example:

```python
individual_scores: Annotated[list[int], operator.add]
```

If three parallel nodes return:

```text
[8]
[7]
[9]
```

the reducer combines them into:

```text
[8, 7, 9]
```

Without an appropriate reducer, multiple updates to the same state field can conflict.

## Example Workflows

### Batsman Analysis

Three calculations are independent:

```text
             ┌──→ Calculate Strike Rate ───┐
             │                             │
START ───────┼──→ Calculate Balls/Boundary ┼──→ Summary → END
             │                             │
             └──→ Calculate Boundary % ────┘
```

The summary node uses the results produced by all three calculations.

### UPSC Essay Evaluation

Different aspects of the essay can be evaluated independently:

```text
             ┌──→ Language Evaluation ──┐
             │                          │
START ───────┼──→ Analysis Evaluation ──┼──→ Final Evaluation → END
             │                          │
             └──→ Clarity Evaluation ───┘
```

Each evaluator produces its own feedback and score. The final node combines the feedback and calculates the average score.

## Main Learning

> **Parallel workflows are useful when multiple tasks are independent and do not need each other's results.**

The key mental model:

> **Fan-out = Split | Parallel Nodes = Work | Reducer = Combine | Fan-in = Continue**

### Important Design Rule

Use **parallelism when tasks are independent**.

If Node B requires the output of Node A, they should remain sequential:

```text
A → B
```

If A, B, and C do not depend on each other:

```text
    ┌→ A ─┐
START → B ─┼→ D
    └→ C ─┘
```

This is where LangGraph starts becoming more than a simple sequential workflow: **the graph can represent both control flow and concurrency.**
