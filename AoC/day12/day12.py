import time
from collections import deque


def read_input():
    file_path = "day12.txt"
    try:
        with open(file_path, 'r') as f:
            grid = [list(line) for line in f.read().splitlines()]
        return grid
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}


def solve(grid):
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
    # part2way1 = sum(len(region) * sidesway1(region) for region in regions) -broenje na strani
    part2way2 = sum(len(region) * sidesway2(region) for region in regions) #broenje na kjoshinja

    return part1, part2way2


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


def main():
    grid = read_input()

    if not grid:
        return

    # Calculate total prices using number of sides and bulk discount sides
    start_time = time.time()
    part1_price, part2_price = solve(grid)
    execution_time = time.time() - start_time

    print(f"Part 1 - Total Fence Price: {part1_price}")
    print(f"Part 2 - Bulk Discount Price: {part2_price}")
    print(f"(Execution Time: {execution_time * 1000:.8f} ms)")


if __name__ == "__main__":
    main()
