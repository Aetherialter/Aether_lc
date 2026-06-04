from os import startfile
import subprocess


SOLUTION_FILE = "solution.py"

SOLUTION_IMPORTS = """from typing import *
from collections import Counter, defaultdict, deque
from functools import cache, lru_cache
from itertools import accumulate, combinations, permutations, product
from bisect import bisect_left, bisect_right, insort
from heapq import heapify, heappop, heappush
from math import gcd, inf, isqrt, lcm
"""
SOLUTION_CASE = """
def run_cases() -> None:
    solution = Solution()
    # Add local assertions here, for example:
    # assert solution.twoSum([2, 7, 11, 15], 9) == [0, 1]
    pass


if __name__ == "__main__":
    run_cases()
"""


def build_solution_content(python_code: str) -> str:
    return f"{SOLUTION_IMPORTS}\n\n{python_code.rstrip()}\n\n{SOLUTION_CASE}\n"


def write_solution_file(python_code: str) -> None:
    with open(SOLUTION_FILE, "w", encoding="utf-8") as file:
        file.write(build_solution_content(python_code))
    startfile(SOLUTION_FILE)


def run_solution_file() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["uv", "run", "python", str(SOLUTION_FILE)],
        capture_output=True,
        text=True,
    )
