import time

def part1(data):
    return solve(data, offset=0)

def part2(data):
    return solve(data, offset=10**13)

def solve(data, offset):
    groups = '\n'.join(data).split('\n\n')
    total = 0

    for group in groups:
        buttonA, buttonB, buttonP = group.split('\n')
        axStr, ayStr = buttonA[10:].split(', ')
        bxStr, byStr = buttonB[10:].split(', ')
        pxStr, pyStr = buttonP[7:].split(', ')

        ax = int(axStr[2:])
        ay = int(ayStr[2:])
        bx = int(bxStr[2:])
        by = int(byStr[2:])
        px = int(pxStr[2:]) + offset
        py = int(pyStr[2:]) + offset

        # Cramer's rule
        denominator = (ax * by - ay * bx) # determinant
        if denominator == 0:
            continue

        m = (px * by - py * bx) // denominator
        if m * denominator != (px * by - py * bx):
            continue

        n = (py - ay * m) // by
        if n * by != (py - ay * m):
            continue

        #Diophantine equation with the solutions by Cramer's rule
        total += 3 * m + n

    return total

def main():
    try:
        with open("day13.txt", "r") as file:
            data = file.read().strip().split('\n')
    except FileNotFoundError:
        print("File not found in the specified path.")
        return

    start_time = time.time()
    part1_result = part1(data)
    part1_time = time.time() - start_time
    print(f"Part 1: {part1_result:} (Time: {part1_time * 1000:.4f} ms)")

    start_time = time.time()
    part2_result = part2(data)
    part2_time = time.time() - start_time
    print(f"Part 2: {part2_result:} (Time: {part2_time * 1000:.4f} ms)")

if __name__ == "__main__":
    main()
