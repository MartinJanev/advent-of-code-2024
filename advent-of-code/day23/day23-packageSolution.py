from time import perf_counter_ns
import os
from itertools import combinations
import networkx as nx

#networkx solution

# Result: 1366 - Time: 12.5082 milliseconds
# Result: bs,cf,cn,gb,gk,jf,mp,qk,qo,st,ti,uc,xw - Time: 8.1175 milliseconds

input_file = os.path.join(os.path.dirname(__file__), "day23.txt")


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


def read_data(file_path):
    with open(file_path) as file:
        return [line.strip() for line in file.readlines()]


@profiler
def find_triangles_with_t(data):
    G = nx.Graph(line.split("-") for line in data)
    cliques = list(nx.find_cliques(G))

    conn = set()
    for clique in cliques:
        for a, b, c in combinations(clique, 3):
            if (
                    "t" in (a[0], b[0], c[0])
                    and (a, b) in G.edges()
                    and (b, c) in G.edges()
                    and (c, a) in G.edges()
            ):
                conn.add(tuple(sorted((a, b, c))))

    return len(conn)


@profiler
def find_largest_clique(data):
    G = nx.Graph(line.split("-") for line in data)
    cliques = list(nx.find_cliques(G))

    largest_clique = max(cliques, key=len)
    return ",".join(sorted(largest_clique))


if __name__ == "__main__":
    data = read_data(input_file)
    find_triangles_with_t(data)
    find_largest_clique(data)