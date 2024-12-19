from functools import cache
import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day11.txt")


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


def read_data(file_path):
    with open(file_path) as file:
        input_data = file.read().strip()
        return [int(x) for x in input_data.split(" ")]


@profiler
def part1(stones):
    for _ in range(25):
        output = []
        for stone in stones:
            if stone == 0:
                output.append(1)
                continue
            string = str(stone)
            length = len(string)
            if length % 2 == 0:
                output.append(int(string[:length // 2]))
                output.append(int(string[length // 2:]))
            else:
                output.append(stone * 2024)
        stones = output

    return len(stones)


@cache
def part2Solver(stone, blinks):
    if blinks == 0:
        return 1
    if stone == 0:
        return part2Solver(1, blinks - 1)
    string = str(stone)
    length = len(string)

    if length % 2 == 0:
        return part2Solver(int(string[:length // 2]), blinks - 1) + part2Solver(int(string[length // 2:]), blinks - 1)
    else:
        return part2Solver(stone * 2024, blinks - 1)


@profiler
def part2():
    return sum(part2Solver(stone, 75) for stone in stones)


if __name__ == "__main__":
    stones = read_data(input_file)
    part1(stones)
    part2()
