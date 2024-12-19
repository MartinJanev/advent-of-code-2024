from time import perf_counter_ns
import os
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day19.txt")


# Method for time profiling
def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start = perf_counter_ns()
        result = method(*args, **kwargs)
        end = perf_counter_ns() - start
        time_len = min(9, ((len(str(end)) - 1) // 3) * 3)
        timeConv = {9: 'seconds', 6: 'milliseconds', 3: 'microseconds', 0: 'nanoseconds'}
        print(f"Result: {result} - Time: {end / (10 ** time_len)} {timeConv[time_len]}")
        return result

    return wrapper_method


def parse_input(file_path):
    with open(file_path, "r") as f:
        lines = f.read().strip().split("\n")

    colorPatterns = lines[0].split(", ")
    designs = lines[2:]
    return colorPatterns, designs


def solver(design, patterns):
    patterns = set(patterns)
    n = len(design)
    dp = {0: 1}  # Base case: one way to form an empty string

    for i in range(1, n + 1):
        dp[i] = 0
        for j in range(i):
            # Check if the substring design[j:i] is in the set of patterns
            if design[j:i] in patterns:
                dp[i] += dp[j]
    return dp[n]


@profiler
def solve():
    patterns, designs = parse_input(input_file)
    count = 0
    total_arrangements = 0
    for design in designs:
        res = solver(design, patterns)
        if res > 0:
            count += 1
        total_arrangements += res
    return " - ".join(map(str, [count, total_arrangements]))


if __name__ == "__main__":
    solve()
