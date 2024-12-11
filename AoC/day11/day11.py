import time
from collections import defaultdict


def split_stone(stone):
    numberOfDigits = len(str(stone))
    m = numberOfDigits // 2
    l = stone // (10 ** m)
    r = stone % (10 ** m)
    return l, r


def solve(stones, blinks):
    stone_counts = defaultdict(int)

    # Initialize the stone counts
    for stone in stones:
        stone_counts[stone] += 1

    for _ in range(blinks):
        afterStone = defaultdict(int)
        for stone, count in stone_counts.items():
            if stone == 0:
                afterStone[1] += count
            elif len(str(stone)) % 2 == 0:
                left, right = split_stone(stone)
                afterStone[left] += count
                afterStone[right] += count
            else:
                afterStone[stone * 2024] += count
        stone_counts = afterStone

    # Total stones is the sum of all counts
    return sum(stone_counts.values())  # sum of all counts in the dictionary for number of stones


def main():
    try:
        with open("day11.txt", "r") as file:
            input_data = file.read().strip()
            stones = list(map(int, input_data.split()))
    except FileNotFoundError:
        print("File not found in the specified path.")
        return

    # Part 1
    start_time = time.time()
    part1_result = solve(stones, 25)  # part 1
    part1_time = time.time() - start_time
    print(f"Part 1: (Time: {part1_time * 1000:.8f} ms) {part1_result:}")

    # Part 2
    start_time = time.time()
    part2_result = solve(stones, 75)  # part 2
    part2_time = time.time() - start_time
    print(f"Part 2: (Time: {part2_time * 1000:.8f} ms) {part2_result:}")


if __name__ == "__main__":
    main()
