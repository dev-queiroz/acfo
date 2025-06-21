# ACFO Architecture

The **Adaptive Code Flow Optimizer (ACFO)** is a Python framework designed to dynamically optimize the execution order
of function calls. This document provides a technical overview of ACFO's architecture, its mathematical foundations, and
its core components.

## Overview

ACFO enhances Python program performance by:

- Parsing code to build a Control Flow Graph (CFG).
- Profiling runtime metrics (execution time and frequency).
- Reordering function calls based on a cost-frequency heuristic while respecting dependencies.

## Mathematical Foundations

ACFO models a program as a directed graph \( G = (V, E) \), where:

- \( V \): Set of functions (nodes).
- \( E \): Dependencies (edges, e.g., \( a \to b \) if `a` calls `b`).
- \( \text{cost}(v) \): Average execution time of function \( v \).
- \( \text{freq}(v) \): Number of calls to function \( v \).

The optimization objective is to minimize total execution time:
\[
\text{Total Cost} = \sum_{v \in V} \text{freq}(v) \cdot \text{cost}(v)
\]
Subject to dependency constraints (e.g., `a` must precede `b` if \( a \to b \)).

ACFO uses a greedy heuristic to prioritize functions:
\[
h(v) = \text{freq}(v) \cdot \text{cost}(v)
\]
Functions with higher \( h(v) \) are executed first, ensuring costly operations are optimized while maintaining
dependency order.

## Components

ACFO consists of three core components:

1. **Parser**:
    - **Purpose**: Extracts function definitions and dependencies from Python code.
    - **Implementation**: Uses the `ast` module to parse code into an Abstract Syntax Tree (AST).
    - **Output**: A CFG stored as a `defaultdict` mapping functions to their dependencies (e.g., `{'a': ['b']}`).

2. **Profiler**:
    - **Purpose**: Collects runtime metrics (execution time and frequency).
    - **Implementation**: Uses `time.time()` to measure execution duration and tracks call counts.
    - **Output**: Dictionaries `costs` (time per function) and `freq` (call counts).

3. **Optimizer**:
    - **Purpose**: Reorders function calls based on the heuristic \( h(v) \).
    - **Implementation**: Uses `heapq` for prioritization and ensures dependencies are respected.
    - **Output**: An optimized call sequence (e.g., `['a', 'b', 'a', 'b', ...]`).

## Workflow

1. **Parse**: The `parse_code` method processes Python code to build the CFG and identify dependencies.
2. **Profile**: The `monitor_execution` method tracks execution time and frequency during initial runs.
3. **Optimize**: The `optimize` method computes priorities (\( h(v) \)) and orders functions.
4. **Execute**: The `execute_optimized` method runs functions in the optimized order, respecting dependencies.

### Example Workflow

For the code:

```python
def a():
    time.sleep(0.1)
    b()


def b():
    time.sleep(0.05)
```

- **Parse**: CFG: `{'a': ['b']}`.
- **Profile**: After 10 calls each, `costs = {'a': ~1.0, 'b': ~0.5}`, `freq = {'a': 10, 'b': 10}`.
- **Optimize**: Priority: `h(a) = 10 \cdot 1.0 \approx 10`, `h(b) = 10 \cdot 0.5 \approx 5`. Order: `['a', 'b']`.
- **Execute**: Optimized calls: `['a', 'b', 'a', 'b', ..., 'a', 'b']`.

## Implementation Details

- **Parsing**: The `ast.NodeVisitor` traverses the AST to detect function calls within definitions.
- **Profiling**: Execution time is measured with millisecond precision using `time.time()`.
- **Optimization**: A greedy algorithm prioritizes high-cost functions, with dependency checks ensuring correctness.
- **Data Structures**:
    - `defaultdict` for CFG and dependencies.
    - `heapq` for maintaining a priority queue of functions.
    - Dictionaries for costs and frequencies.

## Future Enhancements

- **Loop Optimization**: Extend parsing to handle `ast.For` and `ast.While` for loop-aware optimization.
- **Memory Profiling**: Integrate `psutil` to include memory usage in the heuristic.
- **Visualization**: Generate CFG diagrams using `networkx` and `matplotlib`.
- **Dynamic Tracing**: Use `sys.settrace` for real-time optimization suggestions.

## References

- Python `ast` module: [docs.python.org/3/library/ast.html](https://docs.python.org/3/library/ast.html)
- Graph theory in optimization: Cormen et al., *Introduction to Algorithms*.
- Runtime profiling: Python `time` module.

---

*This document is part of the ACFO project. See [README.md](../README.md) for more information.*