import os
from time import perf_counter_ns
from typing import Any
from collections import deque
import heapq

input_file = os.path.join(os.path.dirname(__file__), "day16.txt")


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
        return [list(line.strip()) for line in file.readlines()]


# More intuitive solution

def find(data):
    rows = len(data)
    cols = len(data[0])

    for r in range(rows):
        for c in range(cols):
            if data[r][c] == "S":
                sr = r
                sc = c
                break
            else:
                continue
    return sr, sc


@profiler
def part1(data):
    sr, sc = find(data)

    pq = [(0, sr, sc, 0, 1)]
    seen = {(sr, sc, 0, 1)}

    while pq:
        cost, r, c, dr, dc = heapq.heappop(pq)
        seen.add((r, c, dr, dc))
        if data[r][c] == "E":
            return cost
        for new_cost, nr, nc, ndr, ndc in [(cost + 1, r + dr, c + dc, dr, dc),
                                           (cost + 1000, r, c, dc, -dr),
                                           (cost + 1000, r, c, -dc, dr)]:
            if data[nr][nc] == "#": continue
            if (nr, nc, ndr, ndc) in seen: continue
            heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))


@profiler
def part2(data):
    sr, sc = find(data)

    pq = [(0, sr, sc, 0, 1)]
    lowestCost = {(sr, sc, 0, 1): 0}
    backtrack = {}
    bestCost = float("inf")
    endStates = set()

    while pq:
        cost, r, c, dr, dc = heapq.heappop(pq)
        if cost > lowestCost.get((r, c, dr, dc), float("inf")): continue
        if data[r][c] == "E":
            if cost > bestCost: break
            bestCost = cost
            endStates.add((r, c, dr, dc))
        for new_cost, nr, nc, ndr, ndc in [(cost + 1, r + dr, c + dc, dr, dc),
                                           (cost + 1000, r, c, dc, -dr),
                                           (cost + 1000, r, c, -dc, dr)]:
            if data[nr][nc] == "#": continue
            lowest = lowestCost.get((nr, nc, ndr, ndc), float("inf"))
            if new_cost > lowest: continue
            if new_cost < lowest:
                backtrack[(nr, nc, ndr, ndc)] = set()
                lowestCost[(nr, nc, ndr, ndc)] = new_cost
            backtrack[(nr, nc, ndr, ndc)].add((r, c, dr, dc))
            heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))

    states = deque(endStates)
    seen = set(endStates)

    while states:
        key = states.popleft()
        for last in backtrack.get(key, []):
            if last in seen: continue
            seen.add(last)
            states.append(last)
    seconds = len({(r, c) for r, c, _, _ in seen})
    return str(seconds) + " seconds"


if __name__ == "__main__":
    data = read_data(input_file)
    part1(data)
    part2(data)

#
# import time
# import numpy as np
# from collections import deque
# DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
#
#
# def read_data(file_path):
# with open(file_path) as file:
#     return file.read()
# def parse_grid(data):
#     return [list(line.strip()) for line in data.splitlines()]
#
#
# def find_position(grid, char):
#     for i, row in enumerate(grid):
#         for j, cell in enumerate(row):
#             if cell == char:
#                 return i, j
#     return None
#
#
# @profiler
# def parse(data):
#     grid = parse_grid(data)
#     rows, cols = len(grid), len(grid[0])
#
#     start = find_position(grid, 'S')
#     end = find_position(grid, 'E')
#
#     # Forwards Dijkstra
#     buckets = [[] for _ in range(1001)]
#     seen = np.full((rows, cols, 4), np.iinfo(np.uint32).max, dtype=np.uint32)
#     cost = 0
#     lowest = np.iinfo(np.uint32).max
#
#     buckets[0].append((start, 0))  # State: (position, direction)
#     seen[start[0], start[1], 0] = 0
#
#     while lowest == np.iinfo(np.uint32).max:
#         index = cost % 1001
#
#         while buckets[index]:
#             position, direction = buckets[index].pop()
#
#             if position == end:
#                 lowest = cost
#                 break
#
#             left = (direction + 3) % 4
#             right = (direction + 1) % 4
#             next_states = [
#                 ((position[0] + DIRECTIONS[direction][0], position[1] + DIRECTIONS[direction][1]), direction, cost + 1),
#                 (position, left, cost + 1000),
#                 (position, right, cost + 1000),
#             ]
#
#             for next_pos, next_dir, next_cost in next_states:
#                 if 0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols and grid[next_pos[0]][
#                     next_pos[1]] != '#' and next_cost < seen[next_pos[0], next_pos[1], next_dir]:
#                     bucket_index = next_cost % 1001
#                     buckets[bucket_index].append((next_pos, next_dir))
#                     seen[next_pos[0], next_pos[1], next_dir] = next_cost
#
#         cost += 1
#
#     # Backwards BFS
#     task = deque()
#     path = np.zeros((rows, cols), dtype=bool)
#
#     for direction in range(4):
#         if seen[end[0], end[1], direction] == lowest:
#             task.append((end, direction, lowest))
#
#     while task:
#         position, direction, cost = task.popleft()
#         path[position[0], position[1]] = True
#         if position == start:
#             continue
#
#         left = (direction + 3) % 4
#         right = (direction + 1) % 4
#         next_states = [
#             ((position[0] - DIRECTIONS[direction][0], position[1] - DIRECTIONS[direction][1]), direction, cost - 1),
#             (position, left, cost - 1000),
#             (position, right, cost - 1000),
#         ]
#
#         for next_pos, next_dir, next_cost in next_states:
#             if 0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols and next_cost == seen[
#                 next_pos[0], next_pos[1], next_dir]:
#                 task.append((next_pos, next_dir, next_cost))
#                 seen[next_pos[0], next_pos[1], next_dir] = np.iinfo(np.uint32).max
#
#     return lowest, int(np.sum(path))
#
#
# if __name__ == "__main__":
#     data = read_data(input_file)
#     parsed_input = parse(data)
#     parse(data)
