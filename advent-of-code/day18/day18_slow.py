import time
from collections import deque

GRID_SIZE = 71


def make_Byte_positions(input_data):
    return [tuple(map(int, line.split(","))) for line in input_data.splitlines()]


def make_grid():
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def part1(byte_positions, grid):
    for x, y in byte_positions[:1024]:
        grid[y][x] = 1

    return bfs(grid, (0, 0), (70, 70))


def bfs(grid, start, end):
    queue = deque([(start[0], start[1], 0)])
    visited = set()
    visited.add(start)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        x, y, steps = queue.popleft()

        if (x, y) == end:
            return steps

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in visited and grid[ny][nx] == 0:
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    return -1


def part2(byte_positions, grid):
    for i, (x, y) in enumerate(byte_positions):
        grid[y][x] = 1

        if bfs(grid, (0, 0), (70, 70)) == -1:
            return f"{x},{y}"

    return "Path never blocked."


def main():
    try:
        with open("day18.txt", "r") as file:
            input_data = file.read().strip()
    except FileNotFoundError:
        return "File not found."

    byte_positions = make_Byte_positions(input_data)
    grid = make_grid()

    start_time = time.time()
    part1_result = part1(byte_positions, grid)
    part1_time = time.time() - start_time
    print(f"Part 1: (Time: {part1_time * 1000:.8f} ms) {part1_result:,}")

    start_time = time.time()
    part2_result = part2(byte_positions, grid)
    part2_time = time.time() - start_time
    print(f"Part 2: (Time: {part2_time * 1000:.8f} ms) {part2_result}")


if __name__ == "__main__":
    main()
