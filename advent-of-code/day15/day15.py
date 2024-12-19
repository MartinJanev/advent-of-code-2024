import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day15.txt")


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


def read_data(file_path, part2):
    with open(file_path) as file:
        grid, moves = file.read().split('\n\n')

    if not part2:
        grid = [list(line) for line in grid.splitlines()]
    else:
        expansion = {"#": "##",
                     "O": "[]",
                     ".": "..",
                     "@": "@."}
        grid = [list("".join(expansion[char] for char in line)) for line in grid.splitlines()]

    moveLine = moves.replace('\n', '')
    return grid, moveLine


def find_robot(grid):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == '@':
                return r, c


@profiler
def solve_part1(grid, moves):
    rows = len(grid)
    cols = len(grid[0])

    r, c = find_robot(grid)

    for move in moves:
        dr = {"^": -1, "v": 1}.get(move, 0)
        dc = {">": 1, "<": -1}.get(move, 0)

        targets = [(r, c)]
        cr = r
        cc = c
        go = True
        while True:
            cr += dr
            cc += dc
            char = grid[cr][cc]
            if char == '#':
                go = False
                break
            if char == 'O':
                targets.append((cr, cc))
            if char == '.':
                break

        if not go: continue
        grid[r][c] = '.'
        grid[r + dr][c + dc] = '@'
        for br, bc in targets[1:]:
            grid[br + dr][bc + dc] = 'O'
        r += dr
        c += dc

    return sum(100 * r + c for r in range(rows) for c in range(cols) if grid[r][c] == 'O')


@profiler
def solve_part2(grid, moves):
    rows = len(grid)
    cols = len(grid[0])

    r, c = find_robot(grid)

    for move in moves:
        dr = {"^": -1, "v": 1}.get(move, 0)
        dc = {">": 1, "<": -1}.get(move, 0)

        targets = [(r, c)]
        go = True
        for cr, cc in targets:
            nr = cr + dr
            nc = cc + dc
            if (nr, nc) in targets: continue
            char = grid[nr][nc]
            if char == '#':
                go = False
                break
            if char == '[':
                targets.append((nr, nc))
                targets.append((nr, nc + 1))
            if char == ']':
                targets.append((nr, nc))
                targets.append((nr, nc - 1))

        if not go: continue

        copy = [list(row) for row in grid]
        grid[r][c] = '.'
        grid[r + dr][c + dc] = '@'

        for br, bc in targets[1:]:
            grid[br][bc] = '.'
        for br, bc in targets[1:]:
            grid[br + dr][bc + dc] = copy[br][bc]

        r += dr
        c += dc

    return sum(100 * r + c for r in range(rows) for c in range(cols) if grid[r][c] == '[')


if __name__ == "__main__":
    a, b = read_data(input_file, False)
    solve_part1(a, b)
    a, b = read_data(input_file, True)
    solve_part2(a, b)
