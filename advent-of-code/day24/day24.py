from time import perf_counter_ns
import os
from typing import Any
import re
from functools import cache
from itertools import combinations

input_file = os.path.join(os.path.dirname(__file__), "day24.txt")


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


# Read the data from the input file
def read_data(file_path):
    with open(file_path) as file:
        return file.read()


@profiler
def run_part1_logic(data: str):
    inputs, gates = data.split("\n\n")

    input_pattern = r"([xy]\d\d): ([10])"
    finished = {}
    for line in inputs.split("\n"):
        match = re.search(input_pattern, line)
        input_name, val = match.groups()
        val = int(val)
        finished[input_name] = val

    gate_pattern = r"([a-z0-9]{3}) ([XORAND]+) ([a-z0-9]{3}) -> ([a-z0-9]{3})"
    ops = set()
    op_list = []
    for line in gates.split("\n"):
        match = re.search(gate_pattern, line)
        x1, op, x2, res = match.groups()
        ops.add((x1, x2, res, op))
        op_list.append((x1, x2, res, op))

    parents = {}
    op_map = {}  # Mapping output name to corresponding operation (XOR, OR, AND)
    for x1, x2, res, op in ops:
        parents[res] = (x1, x2)
        op_map[res] = op

    @cache
    def get_depth(reg):
        if reg in finished:
            return 0
        assert reg in parents
        x1, x2 = parents[reg]
        return max(get_depth(x1), get_depth(x2)) + 1

    vars = [(res, get_depth(res)) for _, _, res, _ in ops]
    vars.sort(key=lambda x: x[1])  # Process lower depth first
    for reg, _ in vars:
        x1, x2 = parents[reg]
        v1, v2 = finished[x1], finished[x2]
        op = op_map[reg]
        val = {
            "XOR": lambda a, b: a ^ b,
            "OR": lambda a, b: a | b,
            "AND": lambda a, b: a & b,
        }[op](v1, v2)
        finished[reg] = val

    regs = list(finished.items())
    regs.sort(key=lambda x: x[0])
    num_out = int(str(regs[-1][0])[-2:]) + 1
    bin_str = "".join(str(val) for _, val in regs[-num_out:])
    return int(bin_str[::-1], 2)


@profiler
def run_part2_logic(text: str):
    inputs, gates = text.split("\n\n")

    gate_pattern = r"([a-z0-9]{3}) ([XORAND]+) ([a-z0-9]{3}) -> ([a-z0-9]{3})"
    op_list = []
    for line in gates.split("\n"):
        match = re.search(gate_pattern, line)
        x1, op, x2, res = match.groups()
        op_list.append((x1, x2, res, op))

    def furthest_made(op_list):
        ops = {}
        for x1, x2, res, op in op_list:
            ops[(frozenset([x1, x2]), op)] = res

        def get_res(x1, x2, op):
            return ops.get((frozenset([x1, x2]), op), None)

        carries = {}
        correct = set()
        prev_intermediates = set()
        for i in range(45):
            pos = f"0{i}" if i < 10 else str(i)
            predigit = get_res(f"x{pos}", f"y{pos}", "XOR")
            precarry1 = get_res(f"x{pos}", f"y{pos}", "AND")
            if i == 0:
                assert predigit == f"z00"
                carries[i] = precarry1
                continue
            digit = get_res(carries[i - 1], predigit, "XOR")
            if digit != f"z{pos}":
                return i - 1, correct

            correct.add(carries[i - 1])
            correct.add(predigit)
            for wire in prev_intermediates:
                correct.add(wire)

            precarry2 = get_res(carries[i - 1], predigit, "AND")
            carry_out = get_res(precarry1, precarry2, "OR")
            carries[i] = carry_out
            prev_intermediates = {precarry1, precarry2}

        return 45, correct

    swaps = set()

    base, base_used = furthest_made(op_list)
    for _ in range(4):
        for i, j in combinations(range(len(op_list)), 2):
            x1_i, x2_i, res_i, op_i = op_list[i]
            x1_j, x2_j, res_j, op_j = op_list[j]
            if "z00" in (res_i, res_j):
                continue
            if res_i in base_used or res_j in base_used:
                continue
            op_list[i] = x1_i, x2_i, res_j, op_i
            op_list[j] = x1_j, x2_j, res_i, op_j
            attempt, attempt_used = furthest_made(op_list)
            if attempt > base:
                swaps.add((res_i, res_j))
                base, base_used = attempt, attempt_used
                break
            op_list[i] = x1_i, x2_i, res_i, op_i
            op_list[j] = x1_j, x2_j, res_j, op_j

    return ",".join(sorted(sum(swaps, start=tuple())))


if __name__ == "__main__":
    text = read_data(input_file)
    run_part1_logic(text)
    run_part2_logic(text)
