from time import perf_counter_ns
import os
from typing import Any
from collections import deque
from math import inf

input_file = os.path.join(os.path.dirname(__file__), "day20.txt")


# Method for time profiling
def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        startTimer = perf_counter_ns()
        result = method(*args, **kwargs)
        endTimer = perf_counter_ns() - startTimer
        time_len = min(9, ((len(str(endTimer)) - 1) // 3) * 3)
        timeConv = {9: 'seconds', 6: 'milliseconds', 3: 'microseconds', 0: 'nanoseconds'}
        print(f"Result: {result} - Time: {endTimer / (10 ** time_len)} {timeConv[time_len]}")
        return result

    return wrapper_method


def read_file(file_path):
    with open(file_path) as file:
        return file.readlines()


def parse_input(data):
    rows, cols = len(data), len(data[0].strip())
    grid = [list(line.strip()) for line in data]
    start = end = None

    # Find start ('S') and end ('E') positions
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (c, r)
            elif grid[r][c] == 'E':
                end = (c, r)

    return grid, start, end


def bfs_distance(track, startPos):
    rows, cols = len(track), len(track[0])
    distances = [[inf] * cols for _ in range(rows)]
    queue = deque([(*startPos, 0)])  # (x, y, cost)

    while queue:
        x, y, cost = queue.popleft()
        if distances[y][x] <= cost:
            continue
        distances[y][x] = cost

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Adjacent points
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and track[ny][nx] != '#':
                queue.append((nx, ny, cost + 1))

    return distances


def count_valid_positions(racetrack, start_distance, end_distance, orig_distance, dx_range, dy_range, max_distance):
    rows, cols = len(racetrack), len(racetrack[0])
    count = 0

    for r in range(rows):
        for c in range(cols):
            if racetrack[r][c] == '#':
                continue
            mid_point_dist = start_distance[r][c]
            if mid_point_dist == inf:
                continue

            for dx in dx_range:
                for dy in dy_range:
                    if abs(dx) + abs(dy) > max_distance:  # Max Manhattan distance condition
                        continue
                    nx, ny = c + dx, r + dy
                    if 0 <= nx < cols and 0 <= ny < rows and racetrack[ny][nx] != '#' and end_distance[ny][nx] != inf:
                        new_distance = mid_point_dist + end_distance[ny][nx] + abs(dx) + abs(dy)
                        if new_distance + 100 <= orig_distance:
                            count += 1
    return count


@profiler
def part1(track, startPos, endPos):
    end_distance = bfs_distance(track, endPos)
    start_distance = bfs_distance(track, startPos)
    orig_distance = end_distance[startPos[1]][startPos[0]]
    dx_range, dy_range = range(-2, 3), range(-2, 3)

    return count_valid_positions(track, start_distance, end_distance, orig_distance, dx_range, dy_range, 2)


@profiler
def part2(track, startPos, endPos):
    end_distance = bfs_distance(track, endPos)
    start_distance = bfs_distance(track, startPos)
    orig_distance = end_distance[startPos[1]][startPos[0]]
    dx_range, dy_range = range(-20, 21), range(-20, 21)

    return count_valid_positions(track, start_distance, end_distance, orig_distance, dx_range, dy_range, 20)


if __name__ == "__main__":
    data_from_file = read_file(input_file)
    grid, start, end = parse_input(data_from_file)
    part1(grid, start, end)
    part2(grid, start, end)
