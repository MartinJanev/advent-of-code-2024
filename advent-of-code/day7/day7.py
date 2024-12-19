from operator import add, mul
import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day7.txt")


def read_data(file_path):
    with open(file_path) as file:
        return [list(map(int, line.replace(':', '').split())) for line in file]


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


def cat(a, b): return int(f"{a}{b}")


def solve(nums, ops):
    if len(nums) == 2:
        return nums[0] == nums[1]

    total, a, b, *rest = nums
    for op in ops:
        if solve([total, op(a, b)] + rest, ops):
            return total
    return 0


@profiler
def par1(data):
    return sum(solve(nums, ops=[add, mul]) for nums in data)


@profiler
def par2(data):
    return sum(solve(nums, ops=[add, mul, cat]) for nums in data)


if __name__ == '__main__':
    data = read_data(input_file)
    par1(data)
    par2(data)
