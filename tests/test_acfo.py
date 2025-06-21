# tests/test_acfo.py
"""Unit tests for ACFO."""

import unittest
from acfo import ACFO
import time


class TestACFO(unittest.TestCase):
    def setUp(self):
        self.acfo = ACFO()
        self.code = """
def a():
    b()
def b():
    pass
"""
        self.acfo.parse_code(self.code)

    def test_parse_dependencies(self):
        """Test parsing of function dependencies."""
        self.assertEqual(dict(self.acfo.dependencies), {'a': ['b']})

    def test_optimize_order(self):
        """Test function prioritization based on cost and frequency."""
        self.acfo.freq = {'a': 10, 'b': 10}
        self.acfo.costs = {'a': 1.0, 'b': 0.5}
        ordered_funcs = self.acfo.optimize()
        self.assertEqual(ordered_funcs, ['a', 'b'])

    def test_execute_optimized_simple(self):
        """Test optimized execution with simple dependency."""

        def a(): time.sleep(0.01); return "A"

        def b(): time.sleep(0.005); return "B"

        functions = {"a": a, "b": b}
        for _ in range(10):
            self.acfo.monitor_execution("a", a)
            self.acfo.monitor_execution("b", b)
        calls = []
        self.acfo.execute_optimized(functions, calls, 20)
        expected = ['a', 'b'] * 10
        self.assertEqual(calls, expected)

    def test_complex_dependency(self):
        """Test parsing and optimization with a -> b -> c."""
        code = """
def a():
    b()
def b():
    c()
def c():
    pass
"""
        self.acfo.parse_code(code)
        self.assertEqual(dict(self.acfo.dependencies), {'a': ['b'], 'b': ['c']})

    def test_execute_optimized_pipeline(self):
        """Test optimized execution with read_data -> transform_data -> write_data."""
        code = """
def read_data():
    transform_data()
def transform_data():
    write_data()
def write_data():
    pass
"""
        self.acfo.parse_code(code)

        def read_data(): time.sleep(0.01); return "data"

        def transform_data(): time.sleep(0.015); return "transformed"

        def write_data(): time.sleep(0.005); return "written"

        functions = {"read_data": read_data, "transform_data": transform_data, "write_data": write_data}
        for _ in range(10):
            self.acfo.monitor_execution("read_data", read_data)
            self.acfo.monitor_execution("transform_data", transform_data)
            self.acfo.monitor_execution("write_data", write_data)
        calls = []
        self.acfo.execute_optimized(functions, calls, 30)
        expected = ['read_data', 'transform_data', 'write_data'] * 10
        self.assertEqual(calls, expected)


if __name__ == "__main__":
    unittest.main()
