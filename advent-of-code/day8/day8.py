from typing import List, Set

import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day8.txt")


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
        return file.read().strip().split("\n")


def get_antenna_positions(lines):
    size_y = len(lines)
    size_x = len(lines[0])

    nodes_dict = {}
    for y in range(size_y):
        for x in range(size_x):
            node = lines[y][x]
            if node != '.':
                if node not in nodes_dict:
                    nodes_dict[node] = []
                nodes_dict[node].append((y, x))
    return nodes_dict


def calculate_antinodes(lines: List[str], include_harmonics: bool) -> int:
    size_y = len(lines)
    size_x = len(lines[0])
    nodes_dict = get_antenna_positions(lines)

    antinode_coords: Set[str] = set()
    for coords in nodes_dict.values():
        for y1, x1 in coords:

            # Add the antenna itself as an antinode for Part 2
            if include_harmonics:
                antinode_coords.add(f"{y1},{x1}")

            for y2, x2 in coords:
                if (y1, x1) == (y2, x2):
                    continue

                i = 1
                while True:
                    ay = y2 + (y2 - y1) * i
                    ax = x2 + (x2 - x1) * i

                    if ay < 0 or ay >= size_y or ax < 0 or ax >= size_x:
                        break

                    antinode_coords.add(f"{ay},{ax}")

                    # In Part 1, calculate only the immediate antinode
                    if not include_harmonics:
                        break

                    i += 1

    return len(antinode_coords)


@profiler
def part1(lines):
    return calculate_antinodes(lines, include_harmonics=False)


@profiler
def part2(lines):
    return calculate_antinodes(lines, include_harmonics=True)


if __name__ == "__main__":
    data = read_data(input_file)
    part1(data)
    part2(data)
