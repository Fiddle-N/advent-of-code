import collections


def read_file():
    with open("input.txt") as f:
        return f.read()


def process_text(text):
    orbits = collections.defaultdict(list)
    objects = set()
    for orbit_text in text.rstrip().split("\n"):
        orbit = orbit_text.split(")")
        orbitee, orbiter = orbit
        orbits[orbitee].append(orbiter)
        orbits[orbiter].append(orbitee)  # make graph undirected
        objects.update(orbit)
    return orbits, objects


def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def find_paths_to_com(orbits, objects):
    paths = []
    for obj in objects:
        obj_paths = find_all_paths(orbits, "COM", obj)
        paths.extend(obj_paths)
    return paths


def calculate_orbits(orbits, objects):
    paths = find_paths_to_com(orbits, objects)
    return sum(len(path) - 1 for path in paths)


def find_shortest_path_linear(graph, start, end):
    dist = {start: [start]}
    q = collections.deque([start])
    while len(q):
        at = q.popleft()
        for next in graph[at]:
            if next not in dist:
                dist[next] = [dist[at], next]
                q.append(next)
    return dist[end]


def flatten(list_, output=None):
    if output is None:
        output = []
    for i in list_:
        if isinstance(i, list):
            flatten(i, output)
        else:
            output.append(i)
    return output


def len_shortest_path_linear(graph, start, end):
    path = find_shortest_path_linear(graph, start, end)
    flat_path = flatten(path)
    return len(flat_path) - 1


def main():
    text = read_file()
    orbits, objects = process_text(text)

    orbit_no = calculate_orbits(orbits, objects)
    print(f"number of orbits: {orbit_no}")

    min_orbital_transfers = len_shortest_path_linear(orbits, "YOU", "SAN") - 2
    print(f"min orbital transfers: {min_orbital_transfers}")


if __name__ == "__main__":
    main()
