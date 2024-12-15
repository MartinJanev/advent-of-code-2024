import time

WIDTH = 101
HEIGHT = 103

arr = [0, 0, 0, 0]
robots = []


def part1(data):
    for line in data:
        if line.strip() == "":
            continue
        pos, vel = line.split()
        px, py = map(int, pos[2:].split(","))
        vx, vy = map(int, vel[2:].split(","))

        nx, ny = px + 100 * vx, py + 100 * vy
        nx = nx % WIDTH
        ny = ny % HEIGHT

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

        robots.append(((px, py), (vx, vy)))

    return arr[0] * arr[1] * arr[2] * arr[3]


def part2():
    seconds = 0
    while True:
        grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        seconds += 1
        bad = False

        for robot in robots:
            position, velocity = robot
            px, py = position
            vx, vy = velocity

            nx, ny = px + seconds * vx, py + seconds * vy

            nx = nx % WIDTH
            ny = ny % HEIGHT

            grid[ny][nx] += 1
            if grid[ny][nx] > 1:
                bad = True

        if not bad:
            return seconds


def main():
    try:
        with open("day14.txt", "r") as file:
            data = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("File not found in the specified path.")
        return

    start_time = time.time()
    part1_result = part1(data)
    part1_time = time.time() - start_time
    print(f"Part 1: {part1_result} (Time: {part1_time * 1000:.4f} ms)")

    start_time = time.time()
    part2_result = part2()
    part2_time = time.time() - start_time
    print(f"Part 2: {part2_result} seconds (Time: {part2_time * 1000:.4f} ms)")


if __name__ == "__main__":
    main()
