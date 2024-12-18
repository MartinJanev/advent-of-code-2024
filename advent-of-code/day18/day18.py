from time import perf_counter_ns
import os
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day18.txt")


def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter_ns()
        result = method(*args, **kwargs)
        stop_time = perf_counter_ns() - start_time
        time_len = min(9, ((len(str(stop_time)) - 1) // 3) * 3)
        time_conversion = {9: 'seconds', 6: 'milliseconds', 3: 'microseconds', 0: 'nanoseconds'}
        print(f"Result: {result} - Time: {stop_time / (10 ** time_len)} {time_conversion[time_len]}")
        return result

    return wrapper_method



def mazeTraverse(pts):
    start = (0, 0)
    end = (70, 70)

    seen = set()
    q = [(start, 0)]

    while q:
        cPos, cDir = q.pop(0)

        if cPos in seen:
            continue

        if cPos == end:
            return cDir

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            np = cPos[0] + dx, cPos[1] + dy
            if 0 <= np[0] <= 70 and 0 <= np[1] <= 70 and np not in seen and np not in pts:
                q.append((np, cDir + 1))

        seen.add(cPos)

    return None


# Optimize the part 1 function
@profiler
def part1():
    points = set()
    with open(input_file) as f:
        for l in f:
            points.add(tuple(map(int, l.strip().split(","))))
            if len(points) == 1024:
                break
    return mazeTraverse(points)


# Optimize the part 2 function
@profiler
def part2():
    points = []
    with open(input_file) as f:
        for l in f:
            points.append(tuple(map(int, l.strip().split(","))))

    lBound = 1024
    uBound = len(points)

    while uBound - lBound > 1:
        l = (uBound + lBound) // 2

        if mazeTraverse(points[:l]):
            lBound = l
        else:
            uBound = l

    x, y = points[lBound]
    return ",".join(map(str, [x, y]))


if __name__ == "__main__":
    part1()
    part2()
