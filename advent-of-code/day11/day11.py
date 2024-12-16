import time
from functools import cache


def part1(stones):
    for _ in range(25):
        output = []
        for stone in stones:
            if stone == 0:
                output.append(1)
                continue
            string = str(stone)
            length = len(string)
            if length % 2 == 0:
                output.append(int(string[:length // 2]))
                output.append(int(string[length // 2:]))
            else:
                output.append(stone * 2024)
        stones = output

    return len(stones)


@cache
def part2(stone, blinks):
    if blinks == 0:
        return 1
    if stone == 0:
        return part2(1, blinks - 1)
    string = str(stone)
    length = len(string)

    if length % 2 == 0:
        return part2(int(string[:length // 2]), blinks - 1) + part2(int(string[length // 2:]), blinks - 1)
    else:
        return part2(stone * 2024, blinks - 1)

def main():
    try:
        with open("day11.txt", "r") as file:
            input_data = file.read().strip()
            stones = [int(x) for x in input_data.split(" ")]
    except FileNotFoundError:
        print("File not found in the specified path.")
        return

    # Part 1
    start_time = time.time()
    part1_result = part1(stones)  # part 1
    part1_time = time.time() - start_time
    print(f"Part 1: (Time: {part1_time * 1000:.8f} ms) {part1_result:}")

    # Part 2
    start_time = time.time()
    part2_result = sum(part2(stone, 75) for stone in stones)  # part 2
    part2_time = time.time() - start_time
    print(f"Part 2: (Time: {part2_time * 1000:.8f} ms) {part2_result:}")

    # Part 1: (Time: 2.99286842 ms)
    # Part 2: (Time: 111.12213135 ms)

    # new solution - but first approach for part one is faster though
    # Part 1: (Time: 158.38479996 ms)
    # Part 2: (Time: 152.03046799 ms)


if __name__ == "__main__":
    main()

# def split_stone(stone):
#     numberOfDigits = len(str(stone))
#     m = numberOfDigits // 2
#     l = stone // (10 ** m)
#     r = stone % (10 ** m)
#     return l, r
#
#
# def solve(stones, blinks):
#     stone_counts = defaultdict(int)
#
#     # Initialize the stone counts
#     for stone in stones:
#         stone_counts[stone] += 1
#
#     for _ in range(blinks):
#         afterStone = defaultdict(int)
#         for stone, count in stone_counts.items():
#             if stone == 0:
#                 afterStone[1] += count
#             elif len(str(stone)) % 2 == 0:
#                 left, right = split_stone(stone)
#                 afterStone[left] += count
#                 afterStone[right] += count
#             else:
#                 afterStone[stone * 2024] += count
#         stone_counts = afterStone
#
#     # Total stones is the sum of all counts
#     return sum(stone_counts.values())  # sum of all counts in the dictionary for number of stones