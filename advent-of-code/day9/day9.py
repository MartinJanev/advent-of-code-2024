from collections import deque
from typing import List

import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day9.txt")


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
        return file.read().strip()


class Block:
    def __init__(self, file_id: int, start: int, length: int):
        self.file_id = file_id
        self.start = start
        self.length = length


@profiler
def part1(line):
    block = 0
    checksum = 0

    for pair in parse_in_pairs(line):
        file_id, length = pair
        checksum += ((length * (block + block + length - 1)) // 2) * file_id
        block += length

    return checksum


def parse_in_pairs(line):
    result = []
    blocks = deque(int(c) for c in line)

    if len(blocks) % 2 == 0:
        blocks.pop()

    tail_id = len(blocks) // 2
    tail_length = blocks.pop()
    blocks.pop()

    file_id = 0
    while blocks:
        size = blocks.popleft()
        result.append((file_id, size))
        file_id += 1

        if blocks:
            gap = blocks.popleft()
            while gap > 0:
                min_gap = min(gap, tail_length)
                result.append((tail_id, min_gap))
                tail_length -= min_gap
                gap -= min_gap

                if tail_length == 0:
                    if blocks:
                        tail_id -= 1
                        tail_length = blocks.pop()
                    else:
                        tail_id = 0
                        tail_length = 9
                    if blocks:
                        blocks.pop()

    result.append((tail_id, tail_length))
    return result


@profiler
def part2(line):
    occupied = []
    free = []

    parse2(line, occupied, free)

    for b in reversed(occupied):
        for f in free:
            if f.start >= b.start:
                break

            if f.length >= b.length:
                b.start = f.start
                f.start += b.length
                f.length -= b.length
                break

    return check2(occupied)


def parse2(input, occupied, free):
    start = 0

    if len(input) % 2 != 0:
        input += "0"

    for file_id in range(len(input) // 2):
        length = int(input[file_id * 2])
        occupied.append(Block(file_id, start, length))
        start += length

        length = int(input[file_id * 2 + 1])
        free.append(Block(-1, start, length))
        start += length


def check2(blocks: List[Block]) -> int:
    checksum = 0

    for block in blocks:
        checksum += ((block.length * (block.start * 2 + block.length - 1)) // 2) * block.file_id

    return checksum


if __name__ == "__main__":
    data = read_data(input_file)
    part1(data)
    part2(data)
