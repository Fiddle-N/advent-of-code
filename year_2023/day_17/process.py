import dataclasses
import enum
import heapq
from typing import Self


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Coords(self.x + other.x, self.y + other.y)


class Direction(enum.Enum):
    UPWARDS = enum.auto()
    RIGHTWARDS = enum.auto()
    DOWNWARDS = enum.auto()
    LEFTWARDS = enum.auto()


STRAIGHT_ON_OFFSETS = {
    Direction.UPWARDS: (Coords(0, -1), Direction.UPWARDS),
    Direction.RIGHTWARDS: (Coords(1, 0), Direction.RIGHTWARDS),
    Direction.DOWNWARDS: (Coords(0, 1), Direction.DOWNWARDS),
    Direction.LEFTWARDS: (Coords(-1, 0), Direction.LEFTWARDS),
}

LEFT_RIGHT_OFFSETS = {
    Direction.UPWARDS: (
        (Coords(-1, 0), Direction.LEFTWARDS),
        (Coords(1, 0), Direction.RIGHTWARDS),
    ),
    Direction.RIGHTWARDS: (
        (Coords(0, -1), Direction.UPWARDS),
        (Coords(0, 1), Direction.DOWNWARDS),
    ),
    Direction.DOWNWARDS: (
        (Coords(-1, 0), Direction.LEFTWARDS),
        (Coords(1, 0), Direction.RIGHTWARDS),
    ),
    Direction.LEFTWARDS: (
        (Coords(0, -1), Direction.UPWARDS),
        (Coords(0, 1), Direction.DOWNWARDS),
    ),
}


MAX_STEPS = 3


def _subsequent_steps(direction_history: list[Direction]) -> int:
    steps = 0
    last_step = None
    for step in reversed(direction_history):
        if last_step is None:
            last_step = step
        elif step != last_step:
            break
        steps += 1
    if steps > MAX_STEPS:
        raise ValueError('Invalid path')
    return steps


@dataclasses.dataclass(frozen=True, order=True)
class PrioritisedItem:
    total_heat_loss: int
    location: Coords = dataclasses.field(compare=False)
    direction_history: list[Direction] = dataclasses.field(compare=False)

    def direction(self) -> Direction | None:
        return self.direction_history[-1] if self.direction_history else None

    def subsequent_steps(self) -> int:
        return _subsequent_steps(self.direction_history)

    def is_restricted(self) -> bool:
        return self.subsequent_steps() == MAX_STEPS


@dataclasses.dataclass(frozen=True)
class VisitedLocation:
    location: Coords
    direction: Direction | None
    subsequent_steps: int


class City:

    def __init__(self, city_input):
        self.city = {}
        city_lines = city_input.splitlines()
        self.width = len(city_lines[0])
        self.height = len(city_lines)
        self.start = Coords(0, 0)
        self.end = Coords(self.width - 1, self.height - 1)
        for y, row in enumerate(city_lines):
            for x, heat_loss in enumerate(row):
                self.city[Coords(x, y)] = int(heat_loss)

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())

    def _get_neighbours(self, item):
        neighbours = []
        direction = item.direction()

        if direction is None:
            # currently at start - pretend direction is down (down or right would work)
            direction = Direction.RIGHTWARDS

        offsets = list(LEFT_RIGHT_OFFSETS[direction])
        if not item.is_restricted():
            offsets.append(STRAIGHT_ON_OFFSETS[direction])

        for offset_coord, offset_dir in offsets:
            neighbour_coord = item.location + offset_coord
            if 0 <= neighbour_coord.x < self.width and 0 <= neighbour_coord.y < self.height:
                neighbours.append((neighbour_coord, offset_dir))
        return neighbours

    def dijkstra(self):
        visited: set[VisitedLocation] = set()
        costs: dict[VisitedLocation, int] = {
            VisitedLocation(location=self.start, direction=None, subsequent_steps=0): 0
        }
        q: list[PrioritisedItem] = []

        heapq.heappush(q, PrioritisedItem(0, self.start, direction_history=[]))

        while q:
            item: PrioritisedItem = heapq.heappop(q)
            location = item.location
            direction = item.direction()
            subsequent_steps = item.subsequent_steps()

            current_visited_state = VisitedLocation(
                location=location,
                direction=direction,
                subsequent_steps=subsequent_steps
            )

            if current_visited_state in visited:
                continue

            for steps in range(subsequent_steps, MAX_STEPS + 1):
                visited.add(
                    VisitedLocation(location=location, direction=direction, subsequent_steps=steps)
                )

            current_visited_states = []
            for steps in range(subsequent_steps + 1):
                current_visited_states.append(
                    VisitedLocation(location=location, direction=direction, subsequent_steps=steps)
                )

            if location == self.end:
                return item.total_heat_loss

            for neighbour_coord, neighbour_dir in self._get_neighbours(item):
                next_direction_history = item.direction_history.copy()
                next_direction_history.append(neighbour_dir)

                next_subsequent_steps = _subsequent_steps(next_direction_history)

                neighbour_visited_state = VisitedLocation(
                    location=neighbour_coord,
                    direction=neighbour_dir,
                    subsequent_steps=next_subsequent_steps
                )

                if neighbour_visited_state in visited:
                    continue

                heat_loss = self.city[neighbour_coord]

                current_costs = [costs.get(state) for state in current_visited_states]
                current_costs = [cost for cost in current_costs if cost is not None]
                current_cost = min(current_costs)

                neighbour_visited_states = []
                for steps in range(next_subsequent_steps, MAX_STEPS + 1):
                    neighbour_visited_states.append(
                        VisitedLocation(location=neighbour_coord, direction=neighbour_dir, subsequent_steps=steps)
                    )

                for state in neighbour_visited_states:
                    old_cost = costs.get(state)
                    new_cost = current_cost + heat_loss

                    if old_cost is None or new_cost < old_cost:
                        heapq.heappush(q, PrioritisedItem(new_cost, neighbour_coord, next_direction_history))
                        for steps in range(next_subsequent_steps, MAX_STEPS + 1):
                            costs[state] = new_cost


def main() -> None:
    city = City.read_file()
    best_heat_loss = city.dijkstra()
    print(
        "Least heat loss incurred:",
        best_heat_loss
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
