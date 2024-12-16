import time


def parse_input(filename, part2):
    grid, moves = open(filename).read().split('\n\n')

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


def main():
    try:
        data, moves = parse_input('day15.txt', False)
        if data is None or moves is None:
            return

        start_time = time.time()
        result_part1 = solve_part1(data, moves)
        elapsed_time = time.time() - start_time

        print(f"Part 1: {result_part1} (Time: {elapsed_time * 1000:.4f} ms)")

        data, moves = parse_input('day15.txt', True)

        start_time2 = time.time()
        result_part2 = solve_part2(data, moves)
        elapsed_time2 = time.time() - start_time2

        print(f"Part 2: {result_part2} (Time: {elapsed_time2 * 1000:.4f} ms)")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
