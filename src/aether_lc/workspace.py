from os import startfile

SOLUTION_FILE = "solution.py"

SOLUTION_IMPORTS = """from typing import *
from collections import Counter, defaultdict, deque
from functools import cache, lru_cache
from itertools import accumulate, combinations, permutations, product
from bisect import bisect_left, bisect_right, insort
from heapq import heapify, heappop, heappush
from math import gcd, inf, isqrt, lcm
"""


def build_solution_content(python_code: str) -> str:
    return f"{SOLUTION_IMPORTS}\n\n{python_code.rstrip()}\n"


def write_solution_file(python_code: str) -> None:
    with open(SOLUTION_FILE, "w", encoding="utf-8") as file:
        file.write(build_solution_content(python_code))
    startfile(SOLUTION_FILE)