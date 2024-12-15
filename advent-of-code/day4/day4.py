def part1(grid):
    rows = len(grid)
    cols = len(grid[0])
    directions = [  # (i,j) - how much place to move in each direction
        (0, 1), (0, -1), (1, 0), (-1, 0),  # Horizontal and vertical shifts
        (1, 1), (-1, -1), (1, -1), (-1, 1)  # Diagonal shifts
    ]
    target = "XMAS"
    count = 0

    # Search the grid for all occurrences of the word "XMAS"
    for i in range(rows):
        for j in range(cols):
            for d in directions:  # all directions
                if matches(grid, i, j, d, target):
                    count += 1
    return count


def matches(grid, x, y, direction, target):
    rows = len(grid)
    cols = len(grid[0])

    moveX = direction[0]
    moveY = direction[1]

    for k in range(len(target)):  # Check if the word "XMAS" can be found in the grid with the specific direction
        new_x = x + k * moveX
        new_y = y + k * moveY

        if (new_x < 0 or new_y < 0 or new_x >= rows or new_y >= cols
                or grid[new_x][new_y] != target[k]):
            return False
    return True


def part2(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    # Check for X-MAS pattern centered at each position in the grid
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if matchesXMASPattern(grid, i, j):
                count += 1
    return count


def matchesXMASPattern(grid, x, y):
    # Center character must be 'A'
    if grid[x][y] != 'A':
        return False

    rows = len(grid)
    cols = len(grid[0])

    if x - 1 < 0 or x + 1 >= rows or y - 1 < 0 or y + 1 >= cols:
        return False

    # naming of booleans are where the M are located (left of A, right of A, above A, below A)

    mLeft = (grid[x - 1][y - 1] == 'M' and grid[x + 1][y + 1] == 'S' and
             grid[x - 1][y + 1] == 'S' and grid[x + 1][y - 1] == 'M')

    mRight = (grid[x - 1][y - 1] == 'S' and grid[x + 1][y + 1] == 'M' and
              grid[x - 1][y + 1] == 'M' and grid[x + 1][y - 1] == 'S')

    mUp = (grid[x - 1][y - 1] == 'M' and grid[x + 1][y + 1] == 'S' and
           grid[x - 1][y + 1] == 'M' and grid[x + 1][y - 1] == 'S')

    mDown = (grid[x - 1][y - 1] == 'S' and grid[x + 1][y + 1] == 'M' and
             grid[x - 1][y + 1] == 'S' and grid[x + 1][y - 1] == 'M')

    return mLeft or mRight or mUp or mDown


def main():
    # Load the input file
    try:
        with open("day4.txt", "r") as f:
            grid_data = []
            for line in f.readlines():
                grid_data.append(line.strip())

        # Convert the grid data into a 2D character array

        grid = []
        for row in grid_data:
            grid.append(list(row))

        # Part 1: Find all "XMAS" occurrences
        part1_result = part1(grid)
        print(f"Part 1 result: {part1_result}")

        # Part 2: Find all "X-MAS" patterns
        part2_result = part2(grid)
        print(f"Part 2 result: {part2_result}")

    except FileNotFoundError:
        print("File not found")


if __name__ == "__main__":
    main()
