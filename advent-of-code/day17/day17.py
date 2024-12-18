import time


def getlines(file):
    try:
        with open(f"{file}", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print("File not found in the specified path.")
        return []


def getdata(data):
    # Skip empty lines
    if not data.strip():
        return ""

    if ": " in data:
        return data.split(": ")[1]
    else:
        return ""  # Return an empty string if the format is incorrect


def combo(a, b, c, value):
    if value < 4:
        return value
    if value == 4:
        return a
    if value == 5:
        return b
    if value == 6:
        return c
    return None


def evaluate(a, b, c, ip, program):
    opcode = program[ip]
    arg = program[ip + 1]
    comb = combo(a, b, c, arg)
    if opcode == 0:
        num = a
        denom = pow(2, comb)
        return None, num // denom, b, c, ip + 2
    elif opcode == 1:
        return None, a, b ^ arg, c, ip + 2
    elif opcode == 2:
        return None, a, comb % 8, c, ip + 2
    elif opcode == 3:
        if a == 0:
            return None, a, b, c, ip + 2
        else:
            return None, a, b, c, arg
    elif opcode == 4:
        return None, a, b ^ c, c, ip + 2
    elif opcode == 5:
        return comb % 8, a, b, c, ip + 2
    elif opcode == 6:
        num = a
        denom = pow(2, comb)
        return None, a, num // denom, c, ip + 2
    elif opcode == 7:
        num = a
        denom = pow(2, comb)
        return None, a, b, num // denom, ip + 2


def run_program(a, b, c, program):
    ip = 0
    res = []
    while ip < len(program) - 1:
        (out, a, b, c, ip) = evaluate(a, b, c, ip, program)
        if out is not None:
            res.append(out)
    return res


def part2(program, cursor, sofar):
    for candidate in range(8):
        if run_program(sofar * 8 + candidate, 0, 0, program) == program[cursor:]:
            if cursor == 0:
                return sofar * 8 + candidate
            ret = part2(program, cursor - 1, sofar * 8 + candidate)
            if ret is not None:
                return ret
    return None


def main():
    # Read the lines from the file
    fileStr = "day17.txt"
    lines = getlines(fileStr)

    if not lines:
        return  # Exit if no lines were read

    # Extract data from file
    a1, b1, c1, program_line = getdata(lines[0]), getdata(lines[1]), getdata(lines[2]), getdata(lines[4])
    a = int(a1)
    b = int(b1)
    c = int(c1)

    program = [int(x) for x in program_line.split(",")]

    # Part 1
    start_time = time.time()
    part1_result = ",".join([str(x) for x in run_program(a, b, c, program)])  # part 1 result
    part1_time = time.time() - start_time
    print(f"Part 2: {part1_result} (Time: {part1_time * 1000:.8f} ms)")

    # Part 2
    start_time = time.time()
    part2_result = part2(program, len(program) - 1, 0)
    part2_time = time.time() - start_time
    print(f"Part 2: {part2_result} (Time: {part2_time * 1000:.8f} ms)")


if __name__ == "__main__":
    main()
