# 8. Iterative Workflows


An **iterative workflow** repeats part of the workflow until a desired condition is met or a maximum number of iterations is reached.

Instead of:

```text
START → Generate → Evaluate → END
```

we can create a loop:

```text
START
  ↓
Generate
  ↓
Evaluate
  ↓
 ├── Approved ─────────→ END
 │
 └── Needs Improvement
          ↓
       Optimize
          ↓
       Evaluate
          ↺
```

The main idea is:

> **Generate → Evaluate → Improve → Evaluate → Repeat**

This is the **Evaluator–Optimizer** pattern.

## New Concepts

| Concept                         | What you should understand                                                     |
| ------------------------------- | ------------------------------------------------------------------------------ |
| **Iterative workflow**          | A workflow can repeatedly execute nodes until a condition is satisfied         |
| **Loop / Cycle**                | An edge can point back to an earlier node                                      |
| `add_conditional_edges()`       | Can decide whether to exit the loop or continue iterating                      |
| **Routing function**            | Determines whether the result is good enough or needs improvement              |
| **Evaluator–Optimizer**         | One component evaluates output while another improves it using feedback        |
| **Feedback loop**               | Evaluation produces feedback that becomes input for the next optimization step |
| **Iteration counter**           | Tracks how many improvement cycles have occurred                               |
| `max_iteration`                 | Provides a safety limit so the workflow cannot loop indefinitely               |
| **History state**               | Stores previous generated outputs and feedback across iterations               |
| `Annotated[list, operator.add]` | Allows multiple updates to a list field to be combined                         |
| `with_structured_output()`      | Forces an LLM response into a defined structured schema                        |
| `Pydantic BaseModel`            | Defines and validates the structure of the evaluator's output                  |

## State Across Iterations

The state is what allows the workflow to **remember what happened during previous steps**.

For example:

```text
iteration = 1
tweet = "First attempt"
feedback = "Not punchy enough"
```

After optimization:

```text
iteration = 2
tweet = "Improved attempt"
feedback = "Still needs improvement"
```

The same state continues flowing through the loop.

### History

The workflow also keeps:

```text
tweet_history
feedback_history
```

so previous attempts and feedback are not lost.

## Routing the Loop

The evaluator produces:

```text
approved
```

or

```text
needs_improvement
```

The routing function then decides:

```text
                 ┌──→ END
Evaluate ────────┤
                 └──→ Optimize → Evaluate
```

There is also a safety condition:

```text
if approved OR iteration >= max_iteration:
    END
else:
    Optimize
```

So the workflow has **two ways to terminate**:

1. The output is good enough.
2. The maximum number of iterations is reached.

## Main Learning

> **Loops allow LangGraph workflows to improve their output through repeated execution and feedback.**

The key mental model:

> **State = Memory | Node = Work | Edge = Flow | Conditional Edge = Decision | Cycle = Repeat**

### Important Design Rule

A loop should always have a **clear exit condition**.

```text
Evaluate
   ↓
Good? ── Yes ──→ END
   │
   No
   ↓
Improve
   ↓
Evaluate
```

Without an exit condition such as approval or `max_iteration`, an iterative workflow could continue indefinitely.
