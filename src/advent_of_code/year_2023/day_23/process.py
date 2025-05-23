import collections
import dataclasses
import enum


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)


class TrailTile(enum.Enum):
    PATH = "."
    FOREST = "#"
    NORTHWARDS_SLOPE = "^"
    EASTWARDS_SLOPE = ">"
    SOUTHWARDS_SLOPE = "v"
    WESTWARDS_SLOPE = "<"


class Directions(enum.Enum):
    NORTH = enum.auto()
    EAST = enum.auto()
    SOUTH = enum.auto()
    WEST = enum.auto()


@dataclasses.dataclass(frozen=True)
class PathSearchItem:
    start: Coords
    end: Coords
    distance: int
    section_distance: int
    prev_location: Coords | None


TRAIL_TILE_SLOPES = {
    TrailTile.NORTHWARDS_SLOPE: Directions.NORTH,
    TrailTile.EASTWARDS_SLOPE: Directions.EAST,
    TrailTile.SOUTHWARDS_SLOPE: Directions.SOUTH,
    TrailTile.WESTWARDS_SLOPE: Directions.WEST,
}


OFFSET_COORDS = {
    Directions.NORTH: Coords(0, -1),
    Directions.EAST: Coords(1, 0),
    Directions.SOUTH: Coords(0, 1),
    Directions.WEST: Coords(-1, 0),
}


class HikingTrails:
    def __init__(self, hiking_trail_input):
        trail_rows = hiking_trail_input.splitlines()

        first_row = trail_rows[0]
        start_x = first_row.index(TrailTile.PATH.value)
        self.start = Coords(start_x, 0)

        end_y = len(trail_rows) - 1
        last_row = trail_rows[-1]
        end_x = last_row.index(TrailTile.PATH.value)
        self.end = Coords(end_x, end_y)

        self.map = {
            Coords(x, y): TrailTile(space)
            for y, row in enumerate(trail_rows)
            for x, space in enumerate(row)
        }


def generate_graph(hiking_trails: HikingTrails):
    path_frontier_stack = [
        PathSearchItem(
            start=hiking_trails.start,
            end=hiking_trails.start,
            distance=0,
            section_distance=0,
            prev_location=None,
        )
    ]
    graph = collections.defaultdict(dict)
    visited_junctions = {}

    while path_frontier_stack:
        path_frontier = path_frontier_stack.pop()

        location = path_frontier.end
        space = hiking_trails.map[path_frontier.end]

        if location == hiking_trails.start:
            path_frontier_stack.append(
                PathSearchItem(
                    start=path_frontier.start,
                    end=location + OFFSET_COORDS[Directions.SOUTH],
                    distance=path_frontier.distance + 1,
                    section_distance=0,
                    prev_location=location,
                )
            )
        elif location == hiking_trails.end:
            # save current path and end
            graph[path_frontier.start][location] = path_frontier.distance
        elif space in TRAIL_TILE_SLOPES:
            path_frontier_stack.append(
                PathSearchItem(
                    start=path_frontier.start,
                    end=location + OFFSET_COORDS[TRAIL_TILE_SLOPES[space]],
                    distance=path_frontier.distance + 1,
                    section_distance=0,
                    prev_location=location,
                )
            )
        elif space == TrailTile.PATH:
            surrounding_locations = []
            next_locations = []

            for dir_, coord in OFFSET_COORDS.items():
                surrounding_location = location + coord
                if (
                    new_space := hiking_trails.map[surrounding_location]
                ) != TrailTile.FOREST:
                    surrounding_locations.append(surrounding_location)
                    if surrounding_location != path_frontier.prev_location and (
                        new_space not in TRAIL_TILE_SLOPES
                        or TRAIL_TILE_SLOPES[new_space] == dir_
                    ):
                        next_locations.append(surrounding_location)

            is_junction = all(
                hiking_trails.map[surrounding_location] in TRAIL_TILE_SLOPES
                for surrounding_location in surrounding_locations
            )

            if len(next_locations) > 1 and not is_junction:
                raise ValueError("Unexpected trail")

            if is_junction:
                # we are at a directional_junction
                # ensure we are not going around in a loop
                # where one junction feeds back to a previous one
                if (
                    location in visited_junctions
                    and visited_junctions[location] != path_frontier.section_distance
                ):
                    raise Exception("Loop paths not handled")
                visited_junctions[location] = path_frontier.section_distance

                # save current path
                graph[path_frontier.start][location] = path_frontier.distance

                start = location
                prev_distance = 0
                section_distance = path_frontier.section_distance + 1
            else:
                start = path_frontier.start
                prev_distance = path_frontier.distance
                section_distance = path_frontier.section_distance

            for next_location in next_locations:
                path_frontier_stack.append(
                    PathSearchItem(
                        start=start,
                        end=next_location,
                        distance=prev_distance + 1,
                        section_distance=section_distance,
                        prev_location=location,
                    )
                )
        else:
            raise ValueError

    return graph


def resolve_all_paths(graph, start, end):
    all_paths = []
    path_stack = [(start, {start}, 0)]
    while path_stack:
        path_state = path_stack.pop()
        path_frontier = path_state[0]
        path = path_state[1]
        path_dist = path_state[2]
        next_sections = graph[path_frontier]
        for dest, section_dist in next_sections.items():
            if dest in path:
                continue
            next_path = path.copy()
            next_path.add(dest)
            new_dist = path_dist + section_dist
            if dest == end:
                all_paths.append(new_dist)
            else:
                path_stack.append((dest, next_path, new_dist))
    return all_paths


def find_largest_path(path_vals):
    return max(path_vals)


def di_to_undi_graph(di_graph, start, end):
    # graph will still be directed
    # from start to first node
    # from last node to end
    # and any paths to the penultimate node
    # since there is only one and so when it's reached you go to the end
    # all other paths will be undirected
    penults = []
    for source, dest_nodes in di_graph.items():
        if end in dest_nodes:
            penults.append(source)

    assert len(penults) == 1
    (penult,) = penults

    undi_graph = collections.defaultdict(dict)
    for node_1, dest_nodes in di_graph.items():
        for node_2, dist in dest_nodes.items():
            undi_graph[node_1][node_2] = dist
            if node_1 == start or node_2 == end or node_2 == penult:
                continue
            undi_graph[node_2][node_1] = dist
    return undi_graph


def read_file() -> str:
    with open("input.txt") as f:
        return f.read()


def main():
    hiking_trail_input = read_file()
    hiking_trails = HikingTrails(hiking_trail_input)
    di_graph = generate_graph(hiking_trails)
    paths = resolve_all_paths(
        di_graph, start=hiking_trails.start, end=hiking_trails.end
    )
    largest_path_dist = find_largest_path(paths)
    print(
        "Longest hike length:",
        largest_path_dist,
    )

    undi_graph = di_to_undi_graph(
        di_graph, start=hiking_trails.start, end=hiking_trails.end
    )
    undi_paths = resolve_all_paths(
        undi_graph, start=hiking_trails.start, end=hiking_trails.end
    )
    largest_undi_path_dist = find_largest_path(undi_paths)

    print(
        "Longest hike length where all slopes are normal paths:",
        largest_undi_path_dist,
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
