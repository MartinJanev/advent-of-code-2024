
import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day13.txt")


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
        return file.read().strip().split('\n')


@profiler
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
        denominator = (ax * by - ay * bx)  # determinant
        if denominator == 0:
            continue

        m = (px * by - py * bx) // denominator
        if m * denominator != (px * by - py * bx):
            continue

        n = (py - ay * m) // by
        if n * by != (py - ay * m):
            continue

        # Diophantine equation with the solutions by Cramer's rule
        total += 3 * m + n

    return total


if __name__ == "__main__":
    data = read_data(input_file)
    solve(data, offset=0)
    solve(data, offset=10 ** 13)
