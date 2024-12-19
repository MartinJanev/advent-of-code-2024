import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day17.txt")


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
        return file.readlines()


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


def part2Solver(program, cursor, sofar):
    for candidate in range(8):
        if run_program(sofar * 8 + candidate, 0, 0, program) == program[cursor:]:
            if cursor == 0:
                return sofar * 8 + candidate
            ret = part2Solver(program, cursor - 1, sofar * 8 + candidate)
            if ret is not None:
                return ret
    return None


@profiler
def part2():
    return part2Solver(program, len(program) - 1, 0)


@profiler
def part1():
    return ",".join([str(x) for x in run_program(a, b, c, program)])


if __name__ == "__main__":
    lines = read_data(input_file)
    a, b, = int(getdata(lines[0])), int(getdata(lines[1]))
    c, program = int(getdata(lines[2])), [int(x) for x in getdata(lines[4]).split(",")]
    part1()
    part2()
