import re

def main():
    # Read the data from the file
    data = read_data("day3.txt")

    # Calculate and print results for both parts
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))


if __name__ == "__main__":
    main()


def read_data(file_name):
    try:
        with open(file_name, "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_name} not found!")
    return data


def part1(data):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, "".join(data))

    result = sum(int(x) * int(y) for x, y in matches)

    return result


def part2(data):
    pattern = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"
    instructions = re.findall(pattern, "".join(data))

    enabled = True
    result = 0

    for inst in instructions:
        match inst[0]:
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _ if enabled: #default
                result += int(inst[1]) * int(inst[2])

    return result
