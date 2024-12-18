from time import perf_counter_ns
import os
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day18.txt")


def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter_ns()
        ret = method(*args, **kwargs)
        stop_time = perf_counter_ns() - start_time
        time_len = min(9, ((len(str(stop_time)) - 1) // 3) * 3)
        time_conversion = {9: 'seconds', 6: 'milliseconds', 3: 'microseconds', 0: 'nanoseconds'}
        print(f"Result: {ret} - Time: {stop_time / (10 ** time_len)} {time_conversion[time_len]}")
        return ret

    return wrapper_method


# Maze-solving logic
def maze(pts):
    start = (0, 0)
    end = (70, 70)

    seen = set()
    q = [(start, 0)]

    while q:
        cp, cd = q.pop(0)

        if cp in seen:
            continue

        if cp == end:
            return cd

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            np = cp[0] + dx, cp[1] + dy
            if 0 <= np[0] <= 70 and 0 <= np[1] <= 70 and np not in seen and np not in pts:
                q.append((np, cd + 1))

        seen.add(cp)

    return None


# Optimize the part 1 function
@profiler
def part1():
    pts = set()
    with open(input_file) as f:
        for l in f:
            pts.add(tuple(map(int, l.strip().split(","))))
            if len(pts) == 1024:
                break
    return maze(pts)


# Optimize the part 2 function
@profiler
def part2():
    pts = []
    with open(input_file) as f:
        for l in f:
            pts.append(tuple(map(int, l.strip().split(","))))

    lower = 1024
    upper = len(pts)

    while upper - lower > 1:
        l = (upper + lower) // 2

        if maze(pts[:l]):
            lower = l
        else:
            upper = l

    x, y = pts[lower]
    return ",".join(map(str, [x, y]))


if __name__ == "__main__":
    part1()
    part2()
