import time


def evaluate_expression(numbers, operators, part):
    result = numbers[0]
    for i in range(len(operators)):
        if operators[i] == '+':
            result += numbers[i + 1]
        elif operators[i] == '*':
            result *= numbers[i + 1]
        elif part == "part2" and operators[i] == '|':
            result = int(str(result) + str(numbers[i + 1]))
    return result


def can_match_target(numbers, target, operators, index, part, memo):
    # Base case: end of the operators array, check if the expression matches the target
    if index == len(operators):
        result = evaluate_expression(numbers, operators, part)
        return result == target

    # Check if we've computed this subproblem
    memo_key = (tuple(numbers), target, tuple(operators), index, part)
    if memo_key in memo:
        return memo[memo_key]

    operators[index] = '+'
    if can_match_target(numbers, target, operators, index + 1, part, memo):
        memo[memo_key] = True
        return True

    operators[index] = '*'
    if can_match_target(numbers, target, operators, index + 1, part, memo):
        memo[memo_key] = True
        return True

    if part == "part2":  # Include concatenation operator only for Part 2
        operators[index] = '|'
        if can_match_target(numbers, target, operators, index + 1, part, memo):
            memo[memo_key] = True
            return True

    memo[memo_key] = False
    return False


def process_information(lines, part):
    result = 0
    memo = {}

    for line in lines:
        splitter = line.split(": ")
        target = int(splitter[0])
        numbers = list(map(int, splitter[1].split()))
        operators = [''] * (len(numbers) - 1)

        if can_match_target(numbers, target, operators, 0, part, memo):
            result += target

    return result


def main():
    try:
        with open("day7.txt", "r") as file:
            lines = file.read().strip().split("\n")
    except FileNotFoundError:
        print("File not found in the specified path.")
        return

    part1_result = process_information(lines, "part1")
    print(f"Total Calibration Result (Part 1): {part1_result}")

    start_time = time.time()
    part2_result = process_information(lines, "part2")
    print(f"Total Calibration Result (Part 2): {part2_result}")

    print("Execution Time:", time.time() - start_time, "seconds")


if __name__ == "__main__":
    main()
