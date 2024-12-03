def main():
    try:
        with open("day2.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError("File not found!")

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

    print("Part 1:", numSafeReports)

    for reports in reportBigList:
        if part2(reports):
            numSafeDamperedReports += 1

    print("Part 2:", numSafeDamperedReports)


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
