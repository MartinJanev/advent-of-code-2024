import time
from collections import deque
from typing import List, Tuple


class Block:
    def __init__(self, file_id: int, start: int, length: int):
        self.file_id = file_id
        self.start = start
        self.length = length


def part1(input: str) -> int:
    block = 0
    checksum = 0

    for pair in parse_in_pairs(input):
        file_id, length = pair
        checksum += ((length * (block + block + length - 1)) // 2) * file_id
        block += length

    return checksum


def parse_in_pairs(input: str) -> List[Tuple[int, int]]:
    result = []
    blocks = deque(int(c) for c in input)

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


def part2(input: str) -> int:
    occupied = []
    free = []

    parse2(input, occupied, free)

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


def parse2(input: str, occupied: List[Block], free: List[Block]):
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


def main():
    try:
        with open("day9.txt", "r") as file:
            line = file.read().strip()
    except FileNotFoundError:
        print("File not found in the specified path.")
        return

    start_time = time.time()
    part1_result = part1(line)
    part1_time = time.time() - start_time
    print(f"Part 1: {part1_result:,} (Time: {part1_time * 1000:.4f} ms)")

    # Measure time for Part 2
    start_time = time.time()
    part2_result = part2(line)
    part2_time = time.time() - start_time
    print(f"Part 2: {part2_result:,} (Time: {part2_time * 1000:.4f} ms)")


if __name__ == "__main__":
    main()
