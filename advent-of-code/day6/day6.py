# Result: 4752 - Time: 2.9827 milliseconds
# Result: 1719 - Time: 64.7104039 seconds

from copy import deepcopy
import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day6.txt")

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


def read_data(data):
    try:
        with open(data, "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print("Error: The file 'day6.txt' was not found.")
        return

    return [list(line) for line in lines]


class Position:
    def __init__(self, y, x, facing):
        self.y = y
        self.x = x
        self.facing = facing


# Directions map
DIRECTIONS = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

TURN_RIGHT = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^'
}


def find_start(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in "^v<>":
                return Position(y, x, grid[y][x])
    raise ValueError("Guard start not found")


def walk(grid, start):
    visited = set()
    rows, cols = len(grid), len(grid[0])
    y, x, facing = start.y, start.x, start.facing

    while True:
        state = (y, x, facing)
        if state in visited:
            return visited, True  # Loop detected
        visited.add(state)

        dy, dx = DIRECTIONS[facing]
        new_y, new_x = y + dy, x + dx

        if 0 <= new_y < rows and 0 <= new_x < cols and grid[new_y][new_x] == '#':
            facing = TURN_RIGHT[facing]
        else:
            y, x = new_y, new_x

        if not (0 <= y < rows and 0 <= x < cols):
            return visited, False  # Guard leaves the map


@profiler
def part1(grid):
    start = find_start(grid)
    visited, _ = walk(grid, start)
    return len(set((y, x) for y, x, _ in visited))


@profiler
def part2(grid):
    rows, cols = len(grid), len(grid[0])
    counter = 0

    start = find_start(grid)  # Find start once
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == '.':
                temp_grid = deepcopy(grid)  # Use a copy of the grid
                temp_grid[y][x] = '#'
                visited, loop_detected = walk(temp_grid, start)
                if loop_detected:
                    counter += 1

    return counter


if __name__ == "__main__":
    grid = read_data(input_file)
    if grid:
        part1(grid)
        part2(grid)
