import os
from time import perf_counter_ns
from typing import Any

input_file = os.path.join(os.path.dirname(__file__), "day2.txt")


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


def read_data(file_name):
    try:
        with open(file_name, "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_name} not found!")
    return data


@profiler
def main():
    lines = read_data(input_file)
    reportBigList = []
    for line in lines:
        reports = []
        for i in line.split("\n")[0].split(" "):
            reports.append(i)
        reportBigList.append(reports)

    numSafeReports = 0
    numSafeDamperedReports = 0

    for reports in reportBigList:
        if part1(reports):
            numSafeReports += 1

    for reports in reportBigList:
        if part2(reports):
            numSafeDamperedReports += 1

    return ", ".join(map(str, [numSafeReports, numSafeDamperedReports]))


def part1(report):
    if len(report) < 2:
        return False

    diffrence = int(report[1]) - int(report[0])

    if diffrence > 0:
        flagForIncreasing = 1
    elif diffrence < 0:
        flagForIncreasing = 0

    if abs(diffrence) < 1 or abs(diffrence) > 3:
        return False

    for i in range(2, len(report)):
        getDiff = int(report[i]) - int(report[i - 1])
        if abs(getDiff) < 1 or abs(getDiff) > 3:
            return False

        if getDiff > 0 and flagForIncreasing == 0:
            return False
        if getDiff < 0 and flagForIncreasing == 1:
            return False

    return True


def part2(report):
    if part1(report):
        return True

    for i in range(len(report)):
        modifiedList = report[:i] + report[i + 1:]
        if part1(modifiedList): return True

    return False


if __name__ == "__main__":
    main()
