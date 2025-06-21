"""Example demonstrating ACFO with a data pipeline (read -> transform -> write)."""

from acfo import ACFO
import time


def read_data():
    time.sleep(0.1)
    return "data"


def transform_data():
    time.sleep(0.15)
    return "transformed"


def write_data():
    time.sleep(0.05)
    return "written"


def main():
    code = """
def read_data():
    transform_data()
def transform_data():
    write_data()
def write_data():
    pass
"""
    acfo = ACFO()
    acfo.parse_code(code)

    functions = {
        "read_data": read_data,
        "transform_data": transform_data,
        "write_data": write_data
    }

    calls = []
    for _ in range(10):
        acfo.monitor_execution("read_data", read_data)
        acfo.monitor_execution("transform_data", transform_data)
        acfo.monitor_execution("write_data", write_data)
        calls.append("read_data")
        calls.append("transform_data")
        calls.append("write_data")

    print("Chamadas iniciais:", calls)
    print("Custos:", dict(acfo.costs))
    print("Frequências:", dict(acfo.freq))
    print("Dependências:", dict(acfo.dependencies))

    calls = []
    acfo.execute_optimized(functions, calls, 30)
    print("Chamadas otimizadas:", calls)


if __name__ == "__main__":
    main()
