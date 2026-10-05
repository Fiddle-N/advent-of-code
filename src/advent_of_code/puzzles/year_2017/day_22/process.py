from enum import Enum

from advent_of_code.common import (
    read_file,
    timed_run,
    Coords,
    Direction,
    Turn,
    turn_direction,
    FOUR_POINT_DIRECTION_TO_COORDS,
)

START_LOCATION = Coords(0, 0)
START_DIRECTION = Direction.UP


class Status(Enum):
    CLEAN = "."
    WEAKENED = "W"
    INFECTED = "#"
    FLAGGED = "F"


def parse(raw_nodes: str) -> dict[Coords, Status]:
    # make coordinates signed values
    # such that the centre is 0, 0
    node_list = raw_nodes.splitlines()
    offset = int(len(node_list) / 2)
    nodes = {}
    for y, row in enumerate(node_list):
        for x, node in enumerate(row):
            if Status(node) == Status.INFECTED:
                nodes[Coords(x - offset, y - offset)] = Status.INFECTED
    return nodes


def simulate(nodes: dict[Coords, Status], n_bursts: int):
    nodes = nodes.copy()
    location = START_LOCATION
    dir_ = START_DIRECTION
    caused_infections = 0
    for _ in range(n_bursts):
        turn = Turn.RIGHT if location in nodes else Turn.LEFT
        dir_ = turn_direction(dir_, turn)
        if location in nodes:
            del nodes[location]
        else:
            nodes[location] = Status.INFECTED
            caused_infections += 1
        location = location + FOUR_POINT_DIRECTION_TO_COORDS[dir_]
    return caused_infections


def evolved_simulate(nodes: dict[Coords, Status], n_bursts: int):
    nodes = nodes.copy()
    location = START_LOCATION
    dir_ = START_DIRECTION
    caused_infections = 0
    for _ in range(n_bursts):
        match nodes.get(location, Status.CLEAN):
            case Status.CLEAN:
                dir_ = turn_direction(dir_, Turn.LEFT)
                nodes[location] = Status.WEAKENED
            case Status.WEAKENED:
                # no change to dir
                nodes[location] = Status.INFECTED
                caused_infections += 1
            case Status.INFECTED:
                dir_ = turn_direction(dir_, Turn.RIGHT)
                nodes[location] = Status.FLAGGED
            case Status.FLAGGED:
                # reverse direction
                dir_ = turn_direction(dir_, Turn.LEFT, no_of_turns=2)
                del nodes[location]
        location = location + FOUR_POINT_DIRECTION_TO_COORDS[dir_]
    return caused_infections


def run():
    raw_nodes = read_file()
    nodes = parse(raw_nodes)
    print(simulate(nodes, 10000))
    print(evolved_simulate(nodes, 10000000))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
