"""Example demonstrating ACFO with a simple dependency (a -> b)."""
from acfo import ACFO
import time


def example_function_a():
    time.sleep(0.1)
    return "A"


def example_function_b():
    time.sleep(0.05)
    return "B"


def main():
    code = """
def a():
    b()
def b():
    pass
"""
    acfo = ACFO()
    acfo.parse_code(code)

    functions = {
        "a": example_function_a,
        "b": example_function_b
    }

    calls = []
    for _ in range(10):
        acfo.monitor_execution("a", functions["a"])
        acfo.monitor_execution("b", functions["b"])
        calls.append("a")
        calls.append("b")

    print("Chamadas iniciais:", calls)
    print("Custos:", dict(acfo.costs))
    print("Frequências:", dict(acfo.freq))
    print("Dependências:", dict(acfo.dependencies))

    calls = []
    acfo.execute_optimized(functions, calls, 20)
    print("Chamadas otimizadas:", calls)


if __name__ == "__main__":
    main()
