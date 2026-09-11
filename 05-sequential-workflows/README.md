# 5. Sequential Workflows


A **sequential workflow** executes tasks in a fixed order, where the output of one step can become the input for the next.

```text
START → Node A → Node B → Node C → END
```

LangGraph represents this workflow using **state, nodes, and edges**.

| Concept                 | What you should understand                                                                          |
| ----------------------- | --------------------------------------------------------------------------------------------------- |
| `TypedDict`             | Defines the structure/type of the graph state                                                       |
| `StateGraph`            | Creates a graph that operates on a shared state                                                     |
| `add_node()`            | Registers a function as a node                                                                      |
| `add_edge()`            | Defines the execution path between nodes                                                            |
| `START`                 | Entry point of the graph                                                                            |
| `END`                   | Marks the end of the workflow                                                                       |
| **Node function**       | Reads state, performs work, and returns state/update                                                |
| **State flow**          | Results from one node can be accessed by later nodes                                                |
| `compile()`             | Converts the graph definition into an executable workflow                                           |
| `invoke()`              | Runs the compiled workflow with an initial state                                                    |
| **Sequential workflow** | Nodes execute in a predefined order                                                                 |
| **Prompt chaining**     | Output of one LLM step becomes input/context for the next                                           |
| **LLM node**            | A node can contain an LLM call                                                                      |
| **Non-LLM node**        | A node can also contain normal Python/application logic                                             |
| **Intermediate state**  | Stores results between steps, such as `outline → content → rating`                                  |
| **Evaluation node**     | Can evaluate generated output and store a result such as a `rating`                                 |
| **Evaluator–Optimizer** | Requires evaluation to influence an improvement step; `generate → evaluate → END` is not yet a loop |

## Workflow Structure

```text
Define State
     ↓
Create Nodes
     ↓
Connect Edges
     ↓
Compile
     ↓
Invoke
     ↓
Execute Nodes
     ↓
Update State
     ↓
Final State
```

## Main Learning

> **LangGraph allows us to break a task into nodes, connect them with edges, and pass shared state through the workflow.**

The key mental model:

> **State = Data | Node = Work | Edge = Flow**


