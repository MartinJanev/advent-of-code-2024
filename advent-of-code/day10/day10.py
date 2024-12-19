import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day10.txt")


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
        data = file.read().strip()

    height_map = [list(map(int, line.strip())) for line in data.splitlines()]
    trailheads = [(r, c) for r in range(len(height_map)) for c in range(len(height_map[0])) if height_map[r][c] == 0]
    return data, height_map, trailheads


def recursive_bfs(height_map, r, c, current_height, visited, found_nines, path_count):
    rows, cols = len(height_map), len(height_map[0])
    # If we reach height 9, mark it as a valid trail
    if current_height == 9:
        found_nines.add((r, c))
        path_count[0] += 1
        return

    # Explore neighbors
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
            if height_map[nr][nc] == current_height + 1:
                visited.add((nr, nc))
                recursive_bfs(height_map, nr, nc, height_map[nr][nc], visited, found_nines, path_count)
                visited.remove((nr, nc))


def calculate_score_and_rating(hMap, trailhead):
    found_nines = set()
    path_count = [0]
    visited = {trailhead}
    recursive_bfs(hMap, trailhead[0], trailhead[1], 0, visited, found_nines, path_count)
    return len(found_nines), path_count[0]


@profiler
def part1(hMap, trails):
    return sum(calculate_score_and_rating(hMap, t)[0] for t in trails)


@profiler
def part2(hMap, trails):
    return sum(calculate_score_and_rating(hMap, t)[1] for t in trails)


if __name__ == "__main__":
    data, height_map, trailheads = read_data(input_file)
    part1(height_map, trailheads)
    part2(height_map, trailheads)
