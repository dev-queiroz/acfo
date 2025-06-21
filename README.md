# Adaptive Code Flow Optimizer (ACFO)

The **Adaptive Code Flow Optimizer (ACFO)** is a Python framework that dynamically optimizes the execution order of function calls, prioritizing high-cost operations while respecting dependencies. By leveraging runtime profiling and a Control Flow Graph (CFG), ACFO enhances performance in applications like data pipelines, web servers, and IoT devices without requiring code modifications.

## Key Features
- **Dynamic Optimization**: Reorders function calls based on a heuristic \( h(v) = \text{frequency} \cdot \text{cost} \).
- **Dependency-Aware**: Ensures correct execution order using a CFG parsed with Python's `ast` module.
- **Transparent**: Integrates seamlessly with existing Python code.
- **Open-Source**: Licensed under MIT, welcoming contributions.

## Why Use ACFO?
- **Performance Gains**: Reduces execution time by prioritizing costly functions.
- **Ease of Use**: No need to rewrite code; ACFO profiles and optimizes automatically.
- **Versatility**: Applicable to scientific computing, web development, and embedded systems.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/acfo.git
   cd acfo
   ```
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies (none required currently):
   ```bash
   pip install -r requirements.txt
   ```
4. Install ACFO as a package (optional):
   ```bash
   pip install .
   ```

## Quick Start
Optimize a simple program with two functions:

```python
from acfo import ACFO

def a():
    time.sleep(0.1)  # Simulates a costly task
    return "A"

def b():
    time.sleep(0.05)  # Simulates a lightweight task
    return "B"

acfo = ACFO()
acfo.parse_code("""
def a():
    b()
def b():
    pass
""")
functions = {"a": a, "b": b}
calls = []
for _ in range(10):
    acfo.monitor_execution("a", a)
    acfo.monitor_execution("b", b)
    calls.append("a")
    calls.append("b")
print("Initial Calls:", calls)
calls = []
acfo.execute_optimized(functions, calls, 20)
print("Optimized Calls:", calls)
```

**Expected Output**:
```
Initial Calls: ['a', 'b', 'a', 'b', ..., 'a', 'b']
Optimized Calls: ['a', 'b', 'a', 'b', ..., 'a', 'b']
```

## Use Cases
- **Data Pipelines**: Optimize workflows like `read_data -> transform_data -> write_data` (see `examples/data_pipeline.py`).
- **Web Servers**: Reduce latency in Flask/Django by reordering middleware or route handlers.
- **IoT Devices**: Minimize execution time in resource-constrained environments.

## Project Structure
```
Adaptive-Code-Flow-Optimizer/
├── acfo/               # Core module
│   ├── __init__.py
│   ├── acfo.py
├── examples/           # Example scripts
│   ├── simple_dependency.py
│   ├── data_pipeline.py
├── tests/              # Unit tests
│   ├── test_acfo.py
├── docs/               # Detailed documentation
│   ├── architecture.md
│   ├── contributing.md
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
```

## Contributing
We welcome contributions! Please read [contributing.md](docs/contributing.md) for guidelines on reporting issues, submitting pull requests, and coding standards.

## Documentation
- [Architecture](docs/architecture.md): Technical details and mathematical foundations.
- [Contributing](docs/contributing.md): How to contribute to ACFO.

## License
[MIT License](LICENSE)

## Contact
- **GitHub**: [dev-queiroz](https://github.com/dev-queiroz)
- **Email**: your.email@example.com
- **Issues**: [github.com/dev-queiroz/acfo/issues](https://github.com/dev-queiroz/acfo/issues)

---

*ACFO: Optimize your Python code dynamically, effortlessly, and intelligently.*