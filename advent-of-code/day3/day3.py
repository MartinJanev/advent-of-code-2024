import os
import re
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day3.txt")


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


def read_data(file_name):
    try:
        with open(file_name, "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_name} not found!")
    return data


@profiler
def part1(data):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, "".join(data))

    result = sum(int(x) * int(y) for x, y in matches)

    return result


@profiler
def part2(data):
    pattern = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"
    instructions = re.findall(pattern, "".join(data))

    enabled = True
    result = 0

    for inst in instructions:
        match inst[0]:
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _ if enabled:  # default
                result += int(inst[1]) * int(inst[2])

    return result


if __name__ == "__main__":
    data = read_data(input_file)
    part1(data)
    part2(data)
