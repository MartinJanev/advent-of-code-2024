from time import perf_counter_ns
import os
from typing import List
from collections import defaultdict
from itertools import pairwise

input_file = os.path.join(os.path.dirname(__file__), "day22.txt")


# Method for time profiling
def profiler(method):
    def wrapper_method(*args, **kwargs):
        start = perf_counter_ns()
        result = method(*args, **kwargs)
        end = perf_counter_ns() - start
        time_len = min(9, ((len(str(end)) - 1) // 3) * 3)
        timeConv = {9: 'seconds', 6: 'milliseconds', 3: 'microseconds', 0: 'nanoseconds'}
        print(f"Result: {result} - Time: {end / (10 ** time_len)} {timeConv[time_len]}")
        return result

    return wrapper_method


# Function to read data from file
def read_data(file_path) -> List[int]:
    with open(file_path) as file:
        return [int(line.strip()) for line in file if line.strip()]


# Function to simulate secret number evolution
def evolveSecret(s):
    s ^= s << 6 & 0xFFFFFF
    s ^= s >> 5 & 0xFFFFFF
    return s ^ s << 11 & 0xFFFFFF


@profiler
def part1(values: List[int]) -> int:
    ret = 0
    for s in values:
        nums = [s] + [s := evolveSecret(s) for _ in range(2000)]
        ret += nums[-1]
    return ret


@profiler
def part2(values: List[int]) -> int:
    total = defaultdict(int)
    for s in values:
        nums = [s] + [s := evolveSecret(s) for _ in range(2000)]
        diffs = [b % 10 - a % 10 for a, b in pairwise(nums)]
        seen = set()
        for i in range(len(nums) - 4):
            pat = tuple(diffs[i:i + 4])
            if pat not in seen:
                total[pat] += nums[i + 4] % 10
                seen.add(pat)
    return max(total.values())


# Main execution
if __name__ == "__main__":
    values = read_data(input_file)
    part1(values)
    part2(values)
