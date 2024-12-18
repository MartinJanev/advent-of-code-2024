import time
from copy import deepcopy


class Position:
    def __init__(self, y, x, facing):  # constructor
        self.y = y
        self.x = x
        self.facing = facing


# Directions map
DIRECTIONS = {  # dictionary for what is the incremene/decrement for each direction
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1)
}

TURN_RIGHT = {  # dictionary for turning right
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^'
}


def find_start(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in "^v<>":
                return Position(y, x, grid[y][x])  # return the position of the guard with the direction it is facing
    raise ValueError("Guard start not found")


def part1(grid):
    start = find_start(grid)
    visited = set()
    rows, cols = len(grid), len(grid[0])
    y, x, facing = start.y, start.x, start.facing

    while 0 <= y < rows and 0 <= x < cols:
        visited.add((y, x))
        dy, dx = DIRECTIONS[facing]
        new_y, new_x = y + dy, x + dx

        if 0 <= new_y < rows and 0 <= new_x < cols and grid[new_y][new_x] == '#':
            facing = TURN_RIGHT[facing]
        else:
            y, x = new_y, new_x

    return len(visited)


def part2(grid):
    rows, cols = len(grid), len(grid[0])
    counter = 0

    start = find_start(grid)  # Find start once
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == '.':
                temp_grid = deepcopy(grid)  # Use a copy of the grid
                temp_grid[y][x] = '#'
                if walk_with_obstruction(temp_grid, start):
                    counter += 1

    return counter


def walk_with_obstruction(grid, start):
    visited = set()
    rows, cols = len(grid), len(grid[0])
    y, x, facing = start.y, start.x, start.facing

    while True:
        state = (y, x, facing)
        if state in visited:
            return True  # Loop detected
        visited.add(state)

        dy, dx = DIRECTIONS[facing]
        new_y, new_x = y + dy, x + dx

        if 0 <= new_y < rows and 0 <= new_x < cols and grid[new_y][new_x] == '#':
            facing = TURN_RIGHT[facing]
        else:
            y, x = new_y, new_x

        if not (0 <= y < rows and 0 <= x < cols):
            return False  # Guard leaves the map


def main():
    # Load the grid from the input file
    try:
        with open("day6.txt", "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print("Error: The file 'day6.txt' was not found.")
        return

    grid = [list(line) for line in lines]

    # Part 1: Walk the grid
    result1 = part1(grid)
    print("p1:", result1)

    # Part 2: Try all possible obstruction positions
    start_time = time.time()
    result2 = part2(grid)
    print("p2:", result2)
    print("Execution Time:", time.time() - start_time, "seconds")
    #06.12.2024 implementation: ~under 2minutes xD


if __name__ == "__main__":
    main()
