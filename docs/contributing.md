# Contributing to ACFO

Thank you for your interest in contributing to the **Adaptive Code Flow Optimizer (ACFO)**! We welcome contributions
from the community to make ACFO a powerful tool for Python developers. This guide outlines how to contribute, including
reporting issues, submitting pull requests, and adhering to coding standards.

## How to Contribute

1. **Report Issues**:
    - Use the [Issues](https://github.com/dev-queiroz/acfo/issues) tab on GitHub.
    - Describe the bug or feature request clearly, including:
        - Steps to reproduce (for bugs).
        - Expected vs. actual behavior.
        - Python version and environment.
    - Example:
      ```
      Title: ACFO fails with nested function calls
      Description: When parsing code with nested calls, ACFO misses dependencies.
      Code: def a(): def b(): c(); b()
      Expected: {'a': ['b'], 'b': ['c']}
      Actual: {'a': []}
      ```

2. **Submit Pull Requests (PRs)**:
    - Fork the repository: `https://github.com/dev-queiroz/acfo`.
    - Create a branch: `git checkout -b feature/xyz` or `fix/bug-123`.
    - Make changes and commit: `git commit -m "Add xyz feature"`.
    - Push to your fork: `git push origin feature/xyz`.
    - Open a PR against the `main` branch, describing:
        - What the PR does.
        - Related issue (e.g., `Fixes #123`).
        - Tests added or updated.

3. **Suggest Improvements**:
    - Open a discussion in the [Issues](https://github.com/dev-queiroz/acfo/issues) tab for new features or major
      changes.
    - Examples: Loop optimization, memory profiling, visualization.

## Coding Standards

- **Style**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for code style.
    - Use `black` for formatting: `black .`
    - Check with `flake8`: `flake8 .`
- **Documentation**:
    - Add docstrings for all functions and classes (use NumPy or Google style).
    - Update [architecture.md](architecture.md) for architectural changes.
- **Tests**:
    - Add unit tests in `tests/` using `unittest`.
    - Ensure 100% coverage for new code: `python -m unittest discover tests`
- **Commits**:
    - Write clear, concise commit messages: `Add loop parsing to parse_code`.
    - Group related changes in a single commit.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/acfo.git
   cd acfo
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install development tools:
   ```bash
   pip install black flake8
   ```
5. Run tests:
   ```bash
   python -m unittest discover tests
   ```

## Project Roadmap

- **Short-Term**:
    - Support for loop and conditional parsing (`ast.For`, `ast.While`, `ast.If`).
    - Memory profiling with `psutil`.
    - CFG visualization with `networkx` and `matplotlib`.
- **Long-Term**:
    - Integration with Flask/Django for web optimization.
    - Real-time optimization using `sys.settrace`.
    - Publication as a PyPI package.

## Community Guidelines

- Be respectful and inclusive.
- Provide constructive feedback.
- Acknowledge contributions from others.

## Contact

- **GitHub Issues**: [github.com/dev-queiroz/acfo/issues](https://github.com/dev-queiroz/acfo/issues)
- **Email**: your.email@example.com

---

*Join us in making ACFO a game-changer for Python optimization!*