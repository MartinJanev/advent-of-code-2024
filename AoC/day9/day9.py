import time
from collections import deque


def part1(lines):
    return solve(lines[0], fragmentation=False)


def part2(lines):
    return solve(lines[0], fragmentation=True)


def solve(data, fragmentation):
    blocks = deque([])
    spacesList = deque([])
    file_id = 0
    FINAL = []
    pos = 0
    for i, c in enumerate(data):
        if i % 2 == 0:
            if fragmentation:
                blocks.append((pos, int(c), file_id))
            for _ in range(int(c)):
                FINAL.append(file_id)
                if not fragmentation:
                    blocks.append((pos, 1, file_id))
                pos += 1
            file_id += 1
        else:
            spacesList.append((pos, int(c)))
            for _ in range(int(c)):
                FINAL.append(None)
                pos += 1

    start_time = time.time()
    for (pos, size, file_id) in reversed(blocks):
        for space_i, (space_pos, space_size) in enumerate(spacesList):
            if space_pos < pos and size <= space_size:
                for i in range(size):
                    assert FINAL[pos + i] == file_id, f'{FINAL[pos + i]=}'
                    FINAL[pos + i] = None
                    FINAL[space_pos + i] = file_id
                spacesList[space_i] = (space_pos + size, space_size - size)
                break

    print("Execution Time:", time.time() - start_time, "seconds")
    ans = 0
    for i, c in enumerate(FINAL):
        if c is not None:
            ans += i * c
    return ans


def main():
    try:
        with open("day9.txt", "r") as file:
            lines = file.read().strip().split("\n")
    except FileNotFoundError:
        print("File not found in the specified path.")
        return

    part1_result = part1(lines)
    part2_result = part2(lines)

    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
