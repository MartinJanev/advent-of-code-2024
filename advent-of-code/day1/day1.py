import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day1.txt")


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
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_name} not found!")
    return lines


@profiler
def solve(lines):
    l_list = []
    r_list = []

    r_map = {}

    for line in lines:
        lNum, rNum = map(int, line.strip().split("   "))
        l_list.append(lNum)
        r_list.append(rNum)

        if rNum in r_map:
            r_map[rNum] += 1
        else:
            r_map[rNum] = 1

    l_list.sort()
    r_list.sort()

    sum_part1 = 0
    sum_part1 = sum(abs(l - r) for l, r in zip(l_list, r_list))

    sum_part2 = 0
    sum_part2 += sum(l * r_map[l] for l in l_list if l in r_map)

    return ", ".join(map(str, [sum_part1, sum_part2]))


if __name__ == "__main__":
    data = read_data(input_file)
    solve(data)
