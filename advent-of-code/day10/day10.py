import time


def parse_map(input_map):
    return [list(map(int, line.strip())) for line in input_map.splitlines()]


def find_trailheads(height_map):
    return [(r, c) for r in range(len(height_map)) for c in range(len(height_map[0])) if height_map[r][c] == 0]


def recursive_bfs(height_map, r, c, current_height, visited, found_nines, path_count):
    rows, cols = len(height_map), len(height_map[0])
    # If we reach height 9, mark it as a valid trail
    if current_height == 9:
        found_nines.add((r, c))
        path_count[0] += 1
        return

    # Explore neighbors
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
            if height_map[nr][nc] == current_height + 1:
                visited.add((nr, nc))
                recursive_bfs(height_map, nr, nc, height_map[nr][nc], visited, found_nines, path_count)
                visited.remove((nr, nc))


def calculate_score_and_rating(height_map, trailhead):
    found_nines = set()
    path_count = [0]
    visited = {trailhead}
    recursive_bfs(height_map, trailhead[0], trailhead[1], 0, visited, found_nines, path_count)
    return len(found_nines), path_count[0]


def solve_part1(height_map, trailheads):
    return sum(calculate_score_and_rating(height_map, t)[0] for t in trailheads)


def solve_part2(height_map, trailheads):
    return sum(calculate_score_and_rating(height_map, t)[1] for t in trailheads)


def main():
    try:
        with open("day10.txt", "r") as file:
            input_data = file.read().strip()
    except FileNotFoundError:
        print("File not found in the specified path.")
        return

    height_map = parse_map(input_data)
    trailheads = find_trailheads(height_map)

    # Part 1
    start_time = time.time()
    part1_result = solve_part1(height_map, trailheads)
    part1_time = time.time() - start_time
    print(f"Part 1: (Time: {part1_time * 1000:.8f} ms) {part1_result:,}")

    # Part 2
    start_time = time.time()
    part2_result = solve_part2(height_map, trailheads)
    part2_time = time.time() - start_time
    print(f"Part 2: (Time: {part2_time * 1000:.8f} ms) {part2_result:,}")


if __name__ == "__main__":
    main()
