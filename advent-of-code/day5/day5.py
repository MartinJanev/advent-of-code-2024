from collections import defaultdict, deque


def parse_ordering_rules(file_data):
    rules = defaultdict(set)  # Default to a set for easy additions
    for line in file_data:
        if line.strip() == "":  # Stop parsing rules when encountering an empty line
            break
        before, after = map(int, line.split("|"))
        # before is the page before the pipe, after is the page after the pipe
        rules[before].add(after)  # Add the "after" page to the set of "before" page
    return rules


def parse_updates(file_data):
    updates = []
    toParseAList = False
    for line in file_data:
        if line.strip() == "":
            toParseAList = True  # Start parsing updates after an empty line
            continue
        if toParseAList:
            updates.append(list(map(int, line.split(","))))
    return updates


def is_correctly_ordered(update, rules):
    indexOfPages = {page: i for i, page in enumerate(update)}  # Map each page to its index

    for before, after_set in rules.items():  # Check rules
        for after in after_set:
            if before in indexOfPages and after in indexOfPages and indexOfPages[before] > indexOfPages[after]:  # Rule violation
                return False
    return True


def fix_order(update, rules):
    in_degree = {page: 0 for page in update}  # Initialize in-degree to 0 for all pages
    graph = {page: [] for page in update}  # Adjacency list for dependencies

    # Build graph and in-degree map
    for before, after_set in rules.items():
        for after in after_set:
            if before in in_degree and after in in_degree:  # Consider only pages in the update
                graph[before].append(after)
                in_degree[after] += 1

    queue = deque([page for page, degree in in_degree.items() if degree == 0])
    sorted_order = []

    while queue:
        current = queue.popleft()
        sorted_order.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1  # Decrement in-degree
            if in_degree[neighbor] == 0:  # Add to queue when in-degree becomes 0
                queue.append(neighbor)

    return sorted_order


def get_middle(list):
    return list[len(list) // 2]


def main():
    # Read input data (assuming it's in a file named `day5.txt`)
    with open("day5.txt", "r") as f:
        file_data = f.readlines()

    ordering_rules = parse_ordering_rules(file_data)
    updates = parse_updates(file_data)

    part1 = 0
    part2 = 0

    # Process updates
    for update in updates:
        if is_correctly_ordered(update, ordering_rules):  # Part 1
            part1 += get_middle(update)
        else:  # Part 2
            part2 += get_middle(fix_order(update, ordering_rules))

    # Output results
    print("Total middle page sum of correctly ordered updates:", part1)
    print("Total middle page sum of fixed updates:", part2)


if __name__ == "__main__":
    main()
