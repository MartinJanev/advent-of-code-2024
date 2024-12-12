import time


def read_input():
    file_path = "day12.txt"
    try:
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
        grid = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                grid[x + y * 1j] = c
        return grid
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}


def BFS(grid, start):  # essentially a BFS
    """Performs flood fill on the grid starting from the given position."""
    region = {start}
    letter = grid[start]
    queue = [start]
    while queue:
        pos = queue.pop()
        for dxdy in [1, -1, 1j, -1j]:
            newPos = pos + dxdy
            if newPos in grid and newPos not in region and grid[newPos] == letter:
                region.add(newPos)
                queue.append(newPos)
    return region


def get_area(region):
    """Returns the area of the region."""
    return len(region[1])


def get_perimeter(region):
    """Calculates the perimeter of the region."""
    perimeter = 0
    for pos in region[1]:
        for d in [1, -1, 1j, -1j]:
            new_pos = pos + d
            if new_pos not in region[1]:
                perimeter += 1
    return perimeter


def get_sides_count(region):
    """Counts distinct sides for the given region."""
    perim_obj = set()
    for pos in region[1]:
        for d in [1, -1, 1j, -1j]:
            new_pos = pos + d
            if new_pos not in region[1]:
                perim_obj.add((new_pos, d))

    sides = 0
    while len(perim_obj) > 0:
        pos, d = perim_obj.pop()
        sides += 1
        nextPosition = pos + d * 1j
        while (nextPosition, d) in perim_obj:
            perim_obj.remove((nextPosition, d))
            nextPosition += d * 1j
        nextPosition = pos + d * -1j
        while (nextPosition, d) in perim_obj:
            perim_obj.remove((nextPosition, d))
            nextPosition += d * -1j
    return sides


def part1(grid):
    """Calculates the total fence price using area * perimeter."""
    regions = []
    toCover = set(grid.keys())
    while toCover:
        start = toCover.pop()
        region = BFS(grid, start)
        toCover -= region
        regions.append((grid[start], region))

    price = 0
    for region in regions:
        area, perimeter = get_area(region), get_perimeter(region)
        price += area * perimeter

    return price


def part2(grid):
    """Calculates the total price with a bulk discount using area * sides."""
    regions = []
    uncovered = set(grid.keys())
    while uncovered:
        start = uncovered.pop()
        region = BFS(grid, start)
        uncovered -= region
        regions.append((grid[start], region))

    price = 0
    for region in regions:
        area, sides = get_area(region), get_sides_count(region)
        price += area * sides

    return price


def main():
    grid = read_input()

    if not grid:
        return

    # Part 1: Calculate total price using number of sides
    start_time = time.time()
    part1_price = part1(grid)
    part1_time = time.time() - start_time

    # Part 2: Calculate total price using bulk discount sides
    start_time = time.time()
    part2_price = part2(grid)
    part2_time = time.time() - start_time

    print(f"Part 1 - Total Fence Price: {part1_price} (Execution Time: {part1_time * 1000:.8f} ms)")
    print(f"Part 2 - Bulk Discount Price: {part2_price} (Execution Time: {part2_time * 1000:.8f} ms)")


if __name__ == "__main__":
    main()
