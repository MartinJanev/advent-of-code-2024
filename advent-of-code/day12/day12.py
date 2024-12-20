from collections import deque

import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day12.txt")


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
        return [list(line) for line in file.read().splitlines()]


@profiler
def solve(grid, p2way2):
    rows = len(grid)
    cols = len(grid[0])

    regions = []
    seen = set()

    for r in range(rows):
        for c in range(cols):
            if (r, c) in seen: continue
            seen.add((r, c))
            region = {(r, c)}
            q = deque([(r, c)])
            crop = grid[r][c]
            while q:
                cr, cc = q.popleft()
                for nr, nc in [(cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)]:
                    if nr < 0 or nc < 0 or nr >= rows or nc >= cols: continue
                    if grid[nr][nc] != crop: continue
                    if (nr, nc) in region: continue
                    region.add((nr, nc))
                    q.append((nr, nc))
            seen |= region
            regions.append(region)

    part1 = (sum(len(region) * perimeter(region) for region in regions))
    if p2way2:
        part2 = sum(len(region) * sidesway2(region) for region in regions)  # broenje na kjoshinja
        return part1, "Way 2: " + str(part2)
    else:
        part2 = sum(len(region) * sidesway1(region) for region in regions)  # -broenje na strani
        return part1, "Way 1: " + str(part2)


def perimeter(region):
    output = 0
    for (r, c) in region:
        output += 4
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if (nr, nc) in region:
                output -= 1

    return output


def sidesway1(region):
    edges = {}
    for r, c in region:
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if (nr, nc) in region: continue
            er = (r + nr) / 2
            ec = (c + nc) / 2
            edges[(er, ec)] = (er - r, ec - c)
    seen = set()
    side_count = 0
    for edge, direction in edges.items():
        if edge in seen: continue
        seen.add(edge)
        side_count += 1
        er, ec = edge
        if er % 1 == 0:
            for dr in [-1, 1]:
                cr = er + dr
                while edges.get((cr, ec)) == direction:
                    seen.add((cr, ec))
                    cr += dr
        else:
            for dc in [-1, 1]:
                cc = ec + dc
                while edges.get((er, cc)) == direction:
                    seen.add((er, cc))
                    cc += dc

    return side_count


def sidesway2(region):
    corner_candidates = set()
    for r, c in region:
        for cr, cc in [(r - 0.5, c - 0.5), (r + 0.5, c - 0.5), (r + 0.5, c + 0.5), (r - 0.5, c + 0.5)]:
            corner_candidates.add((cr, cc))
    corners = 0
    for cr, cc in corner_candidates:
        config = [(sr, sc) in region for sr, sc in
                  [(cr - 0.5, cc - 0.5), (cr + 0.5, cc - 0.5), (cr + 0.5, cc + 0.5), (cr - 0.5, cc + 0.5)]]
        number = sum(config)
        if number == 1 or number == 3:
            corners += 1
        elif number == 2:
            if config == [True, False, True, False] or config == [False, True, False, True]:
                corners += 2
    return corners


if __name__ == "__main__":
    grid = read_data(input_file)
    solve(grid, p2way2=False)
    solve(grid, p2way2=True)
