import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day14.txt")


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


def read_data(file_path):
    with open(file_path) as file:
        return [line.strip() for line in file.readlines()]


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


@profiler
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


@profiler
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


if __name__ == "__main__":
    parse_input(read_data(input_file))
    part1()
    part2()
