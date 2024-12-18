import time

WIDTH = 101
HEIGHT = 103

robots = []


def parse_input(data):
    global robots
    for line in data:
        if not line.strip():
            continue
        pos, vel = line.split()
        px, py = map(int, pos[2:].split(","))
        vx, vy = map(int, vel[2:].split(","))
        robots.append(((px, py), (vx, vy)))


def part1():
    arr = [0, 0, 0, 0]
    for robot in robots:
        (px, py), (vx, vy) = robot
        nx, ny = (px + 100 * vx) % WIDTH, (py + 100 * vy) % HEIGHT

        if nx == WIDTH // 2 or ny == HEIGHT // 2:
            continue

        if nx < WIDTH // 2 and ny < HEIGHT // 2:
            arr[0] += 1
        elif nx > WIDTH // 2 and ny < HEIGHT // 2:
            arr[1] += 1
        elif nx < WIDTH // 2 and ny > HEIGHT // 2:
            arr[2] += 1
        else:
            arr[3] += 1

    return arr[0] * arr[1] * arr[2] * arr[3]


def part2():
    seconds = 0
    while True:
        grid = set()  # Use a set for faster lookup
        clashes = False
        seconds += 1

        for robot in robots:
            (px, py), (vx, vy) = robot
            nx, ny = (px + seconds * vx) % WIDTH, (py + seconds * vy) % HEIGHT

            if (nx, ny) in grid:
                clashes = True
                break
            grid.add((nx, ny))

        if not clashes:
            return seconds


def main():
    try:
        with open("day14.txt", "r") as file:
            data = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("File not found.")
        return

    parse_input(data)

    start_time = time.time()
    part1_result = part1()
    part1_time = time.time() - start_time
    print(f"Part 1: {part1_result} (Time: {part1_time * 1000:.4f} ms)")

    start_time = time.time()
    part2_result = part2()
    part2_time = time.time() - start_time
    print(f"Part 2: {part2_result} seconds (Time: {part2_time * 1000:.4f} ms)")


if __name__ == "__main__":
    main()
