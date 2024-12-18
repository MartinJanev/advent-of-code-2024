import time
from typing import List, Dict, Tuple, Set


def get_antenna_positions(lines: List[str]) -> Dict[str, List[Tuple[int, int]]]:
    size_y = len(lines)
    size_x = len(lines[0])

    nodes_dict = {}
    for y in range(size_y):
        for x in range(size_x):
            node = lines[y][x]
            if node != '.':
                if node not in nodes_dict:
                    nodes_dict[node] = []
                nodes_dict[node].append((y, x))
    return nodes_dict


def calculate_antinodes(lines: List[str], include_harmonics: bool) -> int:
    size_y = len(lines)
    size_x = len(lines[0])
    nodes_dict = get_antenna_positions(lines)

    antinode_coords: Set[str] = set()
    for coords in nodes_dict.values():
        for y1, x1 in coords:

            # Add the antenna itself as an antinode for Part 2
            if include_harmonics:
                antinode_coords.add(f"{y1},{x1}")

            for y2, x2 in coords:
                if (y1, x1) == (y2, x2):
                    continue

                i = 1
                while True:
                    ay = y2 + (y2 - y1) * i
                    ax = x2 + (x2 - x1) * i

                    if ay < 0 or ay >= size_y or ax < 0 or ax >= size_x:
                        break

                    antinode_coords.add(f"{ay},{ax}")

                    # In Part 1, calculate only the immediate antinode
                    if not include_harmonics:
                        break

                    i += 1

    return len(antinode_coords)


def part1(lines: List[str]) -> int:
    return calculate_antinodes(lines, include_harmonics=False)


def part2(lines: List[str]) -> int:
    return calculate_antinodes(lines, include_harmonics=True)


def main():
    try:
        with open("day8.txt", "r") as file:
            lines = file.read().strip().split("\n")
    except FileNotFoundError:
        print("File not found in the specified path.")
        return

    start_time = time.time()
    part1_result = part1(lines)
    part1_time = time.time() - start_time
    print(f"Part 1: {part1_result:,} (Time: {part1_time * 1000:.4f} ms)")

    # Measure time for Part 2
    start_time = time.time()
    part2_result = part2(lines)
    part2_time = time.time() - start_time
    print(f"Part 2: {part2_result:,} (Time: {part2_time * 1000:.4f} ms)")


if __name__ == "__main__":
    main()
