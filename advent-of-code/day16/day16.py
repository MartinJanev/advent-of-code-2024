import time
from collections import deque
import numpy as np

# Part 1: 102460, Part2: 527 (Time: 578.38249207 ms)

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse_grid(data):
    return [list(line.strip()) for line in data.splitlines()]


def find_position(grid, char):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == char:
                return i, j
    return None


def parse(data):
    grid = parse_grid(data)
    rows, cols = len(grid), len(grid[0])

    start = find_position(grid, 'S')
    end = find_position(grid, 'E')

    # Forwards Dijkstra
    buckets = [[] for _ in range(1001)]
    seen = np.full((rows, cols, 4), np.iinfo(np.uint32).max, dtype=np.uint32)
    cost = 0
    lowest = np.iinfo(np.uint32).max

    buckets[0].append((start, 0))  # State: (position, direction)
    seen[start[0], start[1], 0] = 0

    while lowest == np.iinfo(np.uint32).max:
        index = cost % 1001

        while buckets[index]:
            position, direction = buckets[index].pop()

            if position == end:
                lowest = cost
                break

            left = (direction + 3) % 4
            right = (direction + 1) % 4
            next_states = [
                ((position[0] + DIRECTIONS[direction][0], position[1] + DIRECTIONS[direction][1]), direction, cost + 1),
                (position, left, cost + 1000),
                (position, right, cost + 1000),
            ]

            for next_pos, next_dir, next_cost in next_states:
                if 0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols and grid[next_pos[0]][
                    next_pos[1]] != '#' and next_cost < seen[next_pos[0], next_pos[1], next_dir]:
                    bucket_index = next_cost % 1001
                    buckets[bucket_index].append((next_pos, next_dir))
                    seen[next_pos[0], next_pos[1], next_dir] = next_cost

        cost += 1

    # Backwards BFS
    todo = deque()
    path = np.zeros((rows, cols), dtype=bool)

    for direction in range(4):
        if seen[end[0], end[1], direction] == lowest:
            todo.append((end, direction, lowest))

    while todo:
        position, direction, cost = todo.popleft()
        path[position[0], position[1]] = True
        if position == start:
            continue

        left = (direction + 3) % 4
        right = (direction + 1) % 4
        next_states = [
            ((position[0] - DIRECTIONS[direction][0], position[1] - DIRECTIONS[direction][1]), direction, cost - 1),
            (position, left, cost - 1000),
            (position, right, cost - 1000),
        ]

        for next_pos, next_dir, next_cost in next_states:
            if 0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols and next_cost == seen[
                next_pos[0], next_pos[1], next_dir]:
                todo.append((next_pos, next_dir, next_cost))
                seen[next_pos[0], next_pos[1], next_dir] = np.iinfo(np.uint32).max

    return lowest, np.sum(path)


def part1(data):
    return data[0]


def part2(data):
    return data[1]


if __name__ == "__main__":
    with open("day16.txt", "r") as f:
        input_data = f.read()

    start_time = time.time()
    parsed_input = parse(input_data)

    part1_result = part1(parsed_input)
    part2_result = part2(parsed_input)
    endtime = time.time() - start_time
    print(f"Part 1: {part1_result}, Part 2: {part2_result} (Time: {endtime * 1000:.8f} ms)")

# More intuitive solution

# Part 1: 102460 (Time: 1590.3578 ms)
# Part 2: 527 seconds (Time: 2568.2993 ms)

# from collections import deque
# import time
# import heapq
#
#
# def find(data):
#     rows = len(data)
#     cols = len(data[0])
#
#     for r in range(rows):
#         for c in range(cols):
#             if data[r][c] == "S":
#                 sr = r
#                 sc = c
#                 break
#             else:
#                 continue
#     return sr, sc
#
#
# def part1(data):
#     sr, sc = find(data)
#
#     pq = [(0, sr, sc, 0, 1)]
#     seen = {(sr, sc, 0, 1)}
#
#     while pq:
#         cost, r, c, dr, dc = heapq.heappop(pq)
#         seen.add((r, c, dr, dc))
#         if data[r][c] == "E":
#             return cost
#         for new_cost, nr, nc, ndr, ndc in [(cost + 1, r + dr, c + dc, dr, dc),
#                                            (cost + 1000, r, c, dc, -dr),
#                                            (cost + 1000, r, c, -dc, dr)]:
#             if data[nr][nc] == "#": continue
#             if (nr, nc, ndr, ndc) in seen: continue
#             heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))
#
#
# def part2(data):
#     sr, sc = find(data)
#
#     pq = [(0, sr, sc, 0, 1)]
#     lowestCost = {(sr, sc, 0, 1): 0}
#     backtrack = {}
#     bestCost = float("inf")
#     endStates = set()
#
#     while pq:
#         cost, r, c, dr, dc = heapq.heappop(pq)
#         if cost > lowestCost.get((r, c, dr, dc), float("inf")): continue
#         if data[r][c] == "E":
#             if cost > bestCost: break
#             bestCost = cost
#             endStates.add((r, c, dr, dc))
#         for new_cost, nr, nc, ndr, ndc in [(cost + 1, r + dr, c + dc, dr, dc),
#                                            (cost + 1000, r, c, dc, -dr),
#                                            (cost + 1000, r, c, -dc, dr)]:
#             if data[nr][nc] == "#": continue
#             lowest = lowestCost.get((nr, nc, ndr, ndc), float("inf"))
#             if new_cost > lowest: continue
#             if new_cost < lowest:
#                 backtrack[(nr, nc, ndr, ndc)] = set()
#                 lowestCost[(nr, nc, ndr, ndc)] = new_cost
#             backtrack[(nr, nc, ndr, ndc)].add((r, c, dr, dc))
#             heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))
#
#     states = deque(endStates)
#     seen = set(endStates)
#
#     while states:
#         key = states.popleft()
#         for last in backtrack.get(key, []):
#             if last in seen: continue
#             seen.add(last)
#             states.append(last)
#     return len({(r, c) for r, c, _, _ in seen})
#
#
# def main():
#     try:
#         with open("day16.txt", "r") as file:
#             data = [list(line.strip()) for line in file.readlines()]
#     except FileNotFoundError:
#         print("File not found in the specified path.")
#         return
#
#     start_time = time.time()
#     part1_result = part1(data)
#     part1_time = time.time() - start_time
#     print(f"Part 1: {part1_result} (Time: {part1_time * 1000:.4f} ms)")
#
#     start_time = time.time()
#     part2_result = part2(data)
#     part2_time = time.time() - start_time
#     print(f"Part 2: {part2_result} seconds (Time: {part2_time * 1000:.4f} ms)")
#
#
# if __name__ == "__main__":
#     main()
