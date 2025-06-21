# acfo/acfo.py
"""Adaptive Code Flow Optimizer (ACFO) for dynamic function call optimization.

This module provides a framework to parse Python code, profile execution, and
optimize function call order based on cost and frequency, respecting dependencies.
"""

import ast
import time
import heapq
from collections import defaultdict


class ACFO:
    """Optimizer for reordering function calls based on runtime metrics.

    Attributes:
        cfg (defaultdict): Control Flow Graph mapping functions to dependencies.
        freq (defaultdict): Frequency of function calls.
        costs (defaultdict): Total execution time per function.
        dependencies (defaultdict): Function dependencies (caller -> callees).
        heap (list): Priority queue for optimization.
    """

    def __init__(self):
        """Initialize ACFO with empty data structures."""
        self.cfg = defaultdict(list)
        self.freq = defaultdict(int)
        self.costs = defaultdict(float)
        self.dependencies = defaultdict(list)
        self.heap = []

    def parse_code(self, code: str) -> ast.AST:
        """Parse Python code into a CFG with dependencies.

        Args:
            code: String containing Python code.

        Returns:
            AST object representing the parsed code.

        Example:
            >>> acfo = ACFO()
            >>> code = "def a():\\n    b()\\ndef b():\\n    pass"
            >>> acfo.parse_code(code)
            >>> acfo.dependencies
            defaultdict(<class 'list'>, {'a': ['b']})
        """
        tree = ast.parse(code)
        self.costs.clear()
        self.dependencies.clear()
        self.cfg.clear()

        class FunctionVisitor(ast.NodeVisitor):
            def __init__(self, acfo):
                self.acfo = acfo
                self.current_func = None

            def visit_FunctionDef(self, node):
                self.current_func = node.name
                self.acfo.costs[node.name] = 0.0
                self.acfo.freq[node.name] = 0
                self.generic_visit(node)
                self.current_func = None

            def visit_Call(self, node):
                if self.current_func and isinstance(node.func, ast.Name):
                    called_func = node.func.id
                    self.acfo.dependencies[self.current_func].append(called_func)
                    self.acfo.cfg[self.current_func].append((called_func, 0.0))
                self.generic_visit(node)

        visitor = FunctionVisitor(self)
        visitor.visit(tree)
        return tree

    def monitor_execution(self, func_name: str, func: callable) -> any:
        """Monitor execution time and frequency of a function.

        Args:
            func_name: Name of the function.
            func: Callable function to execute.

        Returns:
            Result of the function execution.

        Example:
            >>> acfo = ACFO()
            >>> def a(): return "A"
            >>> acfo.monitor_execution("a", a)
            'A'
            >>> acfo.freq["a"]
            1
        """
        start_time = time.time()
        result = func()
        elapsed = time.time() - start_time
        self.costs[func_name] += elapsed
        self.freq[func_name] += 1
        heapq.heappush(self.heap, (-elapsed, func_name))
        return result

    def optimize(self) -> list:
        """Reorder functions based on frequency and cost, respecting dependencies.

        Returns:
            List of function names in optimized order.

        Example:
            >>> acfo = ACFO()
            >>> acfo.freq = {"a": 10, "b": 10}
            >>> acfo.costs = {"a": 1.0, "b": 0.5}
            >>> acfo.optimize()
            ['a', 'b']
        """
        priorities = [(node, self.freq[node] * self.costs[node]) for node in self.freq]
        priorities.sort(key=lambda x: x[1], reverse=True)
        ordered_funcs = [node for node, _ in priorities]

        # Topological sort to respect dependencies
        def topological_sort():
            in_degree = defaultdict(int)
            for func in self.freq:
                for dep in self.dependencies[func]:
                    in_degree[dep] += 1
            queue = [func for func in self.freq if in_degree[func] == 0]
            result = []
            while queue:
                func = queue.pop(0)
                result.append(func)
                for dep in self.dependencies[func]:
                    in_degree[dep] -= 1
                    if in_degree[dep] == 0:
                        queue.append(dep)
            return result

        topo_order = topological_sort()
        final_order = [func for func in topo_order if func in ordered_funcs]
        print(f"Priorities: {priorities}, Ordered funcs: {final_order}")
        return final_order

    def execute_optimized(self, functions: dict, calls: list, num_calls: int) -> list:
        """Execute program with optimized function call order.

        Args:
            functions: Dictionary mapping function names to callables.
            calls: List to store optimized call sequence.
            num_calls: Total number of calls to execute.

        Returns:
            List of optimized function calls.

        Example:
            >>> acfo = ACFO()
            >>> def a(): time.sleep(0.1); return "A"
            >>> def b(): time.sleep(0.05); return "B"
            >>> acfo.parse_code("def a():\\n    b()\\ndef b():\\n    pass")
            >>> functions = {"a": a, "b": b}
            >>> calls = []
            >>> for _ in range(10): acfo.monitor_execution("a", a); acfo.monitor_execution("b", b)
            >>> acfo.execute_optimized(functions, calls, 20)
            ['a', 'b', 'a', 'b', ..., 'a', 'b']
        """
        print("Iniciando execute_optimized...")
        ordered_funcs = self.optimize()
        original_freq = dict(self.freq)
        calls_made = 0

        while calls_made < num_calls:
            print(f"Calls made: {calls_made}, Ordered funcs: {ordered_funcs}")
            executed = False
            # Track functions executed in this iteration to avoid redundant calls
            executed_funcs = set()
            for func_name in ordered_funcs:
                if func_name in functions and original_freq[
                    func_name] > 0 and func_name not in executed_funcs and calls_made < num_calls:
                    # Check if all dependencies have sufficient remaining calls
                    can_execute = True
                    for dep in self.dependencies[func_name]:
                        if original_freq.get(dep, 0) < original_freq[func_name]:
                            can_execute = False
                            break
                    if can_execute:
                        print(f"Executing {func_name}")
                        self.monitor_execution(func_name, functions[func_name])
                        calls.append(func_name)
                        original_freq[func_name] -= 1
                        calls_made += 1
                        executed_funcs.add(func_name)
                        executed = True

                        # Execute dependencies exactly once
                        for dep in self.dependencies.get(func_name, []):
                            if dep in functions and original_freq[dep] > 0 and calls_made < num_calls:
                                print(f"Executing dependency {dep}")
                                self.monitor_execution(dep, functions[dep])
                                calls.append(dep)
                                original_freq[dep] -= 1
                                calls_made += 1
                                executed_funcs.add(dep)

            if not executed:
                break  # Prevent infinite loop if no function can be executed

        print("Finalizando execute_optimized...")
        return calls
