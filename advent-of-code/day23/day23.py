from time import perf_counter_ns
import os

input_file = os.path.join(os.path.dirname(__file__), "day23.txt")


# Result: 1366 - Time: 32.0357 milliseconds
# Result: bs,cf,cn,gb,gk,jf,mp,qk,qo,st,ti,uc,xw - Time: 1.6846 milliseconds

# Method for profiling execution time
def profiler(method):
    def wrapper_method(*args, **kwargs):
        start = perf_counter_ns()
        result = method(*args, **kwargs)
        end = perf_counter_ns() - start
        time_len = min(9, ((len(str(end)) - 1) // 3) * 3)
        time_conv = {9: 'seconds', 6: 'milliseconds', 3: 'microseconds', 0: 'nanoseconds'}
        print(f"Result: {result} - Time: {end / (10 ** time_len)} {time_conv[time_len]}")
        return result

    return wrapper_method


# Read the input data
def read_data(file_path):
    with open(file_path) as file:
        return [line.strip() for line in file.readlines()]


@profiler
def part1(data):
    edges = [line.split("-") for line in data]
    conns = {}

    for x, y in edges:
        if x not in conns: conns[x] = set()
        if y not in conns: conns[y] = set()
        conns[x].add(y)
        conns[y].add(x)

    triangle_count = 0
    vertices = list(conns.keys())

    for i in range(len(vertices) - 2):
        a = vertices[i]
        for j in range(i + 1, len(vertices) - 1):
            b = vertices[j]
            if b not in conns[a]: continue
            for k in range(j + 1, len(vertices)):
                c = vertices[k]
                if c in conns[a] and c in conns[b]:
                    if "t" in {a[0], b[0], c[0]}:
                        triangle_count += 1

    return triangle_count


@profiler
def part2(data):
    edges = [line.split("-") for line in data]
    conns = {}

    for x, y in edges:
        if x not in conns: conns[x] = set()
        if y not in conns: conns[y] = set()
        conns[x].add(y)
        conns[y].add(x)

    def findNetworks(node, candidates, visited):
        network = {node}
        for neighbor in candidates:
            if all(neighbor in conns[member] for member in network):
                network.add(neighbor)
        visited.update(network)
        return network

    largest_network = set()
    visited = set()

    for node in conns:
        if node not in visited:
            candidates = conns[node]
            network = findNetworks(node, candidates, visited)
            if len(network) > len(largest_network):
                largest_network = network

    return ",".join(sorted(largest_network))


if __name__ == "__main__":
    data = read_data(input_file)
    part1(data)
    part2(data)
