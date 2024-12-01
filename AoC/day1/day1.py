def main():
    try:
        with open("day1.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError("File not found!")

    l_list = []
    r_list = []

    r_map = {}

    for line in lines:
        left_side_num, right_side_num = map(int, line.strip().split("   "))
        l_list.append(left_side_num)
        r_list.append(right_side_num)

        if right_side_num in r_map:
            r_map[right_side_num] += 1
        else:
            r_map[right_side_num] = 1

    l_list.sort()
    r_list.sort()

    sum_part1 = 0
    for l, r in zip(l_list, r_list):
        difference = abs(l - r)
        sum_part1 += difference

    sum_part2 = 0
    for l in l_list:
        if l in r_map:
            sum_part2 += l * r_map[l]

    print("Part1: ", sum_part1)
    print("Part2: ", sum_part2)


if __name__ == "__main__":
    main()
