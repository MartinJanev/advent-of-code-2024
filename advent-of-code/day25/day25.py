from time import perf_counter_ns
import os
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day25.txt")


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


@profiler
def process_keys_and_locks() -> int:

    with open(input_file) as file:
        data = file.read().strip()

    keys, locks = [], []

    # Split data into groups and process each
    for thing in map(str.split, data.split('\n\n')):
        if thing[0][0] == '.':
            keys.append([col.count('#') - 1 for col in zip(*thing)])
        elif thing[0][0] == '#':
            locks.append([col.count('#') - 1 for col in zip(*thing)])

    # Calculate and return the result
    return sum(
        all(k[col] + l[col] <= 5 for col in range(5))
        for k in keys for l in locks
    )


if __name__ == "__main__":
    process_keys_and_locks()
