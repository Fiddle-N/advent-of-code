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

    def __mul__(self, other: int) -> Self:
        return Coords(self.x * other, self.y * other)


class Direction(enum.Enum):
    UPWARDS = enum.auto()
    RIGHTWARDS = enum.auto()
    DOWNWARDS = enum.auto()
    LEFTWARDS = enum.auto()


OFFSETS = {
    Direction.UPWARDS: [
        (Coords(-1, 0), Direction.LEFTWARDS),
        (Coords(0, -1), Direction.UPWARDS),
        (Coords(1, 0), Direction.RIGHTWARDS),
    ],
    Direction.RIGHTWARDS: [
        (Coords(0, -1), Direction.UPWARDS),
        (Coords(1, 0), Direction.RIGHTWARDS),
        (Coords(0, 1), Direction.DOWNWARDS),
    ],
    Direction.DOWNWARDS: [
        (Coords(-1, 0), Direction.LEFTWARDS),
        (Coords(0, 1), Direction.DOWNWARDS),
        (Coords(1, 0), Direction.RIGHTWARDS),
    ],
    Direction.LEFTWARDS: [
        (Coords(0, -1), Direction.UPWARDS),
        (Coords(-1, 0), Direction.LEFTWARDS),
        (Coords(0, 1), Direction.DOWNWARDS),
    ],
}


@dataclasses.dataclass(frozen=True)
class LocationState:
    location: Coords
    direction: Direction | None
    straight_steps: int


@dataclasses.dataclass(frozen=True, order=True)
class LocationStateWithHeatLoss:
    heat_loss: int
    location: Coords = dataclasses.field(compare=False)
    direction: Direction | None = dataclasses.field(compare=False)
    straight_steps: int = dataclasses.field(compare=False)


class City:
    def __init__(self, city_input):
        self.city = {}
        city_lines = city_input.splitlines()
        self.width = len(city_lines[0])
        self.height = len(city_lines)
        for y, row in enumerate(city_lines):
            for x, heat_loss in enumerate(row):
                self.city[Coords(x, y)] = int(heat_loss)

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())


class _HeatLossMinimiser:
    def __init__(self, city, min_consec_steps, max_consec_steps):
        self.city = city
        assert min_consec_steps > 0
        assert max_consec_steps >= min_consec_steps
        self.min_consec_steps = min_consec_steps
        self.max_consec_steps = max_consec_steps

        self.start = Coords(0, 0)
        self.end = Coords(self.city.width - 1, self.city.height - 1)

        self.visited: set[LocationState] = set()
        self.costs: dict[LocationState, int] = {
            LocationState(location=self.start, direction=None, straight_steps=0): 0
        }
        self.q: list[LocationStateWithHeatLoss] = []
        heapq.heappush(
            self.q,
            LocationStateWithHeatLoss(
                heat_loss=0, location=self.start, direction=None, straight_steps=0
            ),
        )

    def _is_valid_coord(self, coord: Coords):
        return (0 <= coord.x < self.city.width) and (0 <= coord.y < self.city.height)

    def _traverse_city(
        self, start: Coords, offset: Coords, step_change: int
    ) -> tuple[Coords, int] | None:
        destination = start
        heat_loss = 0
        for _ in range(step_change):
            destination += offset
            if not self._is_valid_coord(destination):
                return None
            heat_loss += self.city.city[destination]
        return destination, heat_loss

    def _get_neighbours(self, item) -> list[LocationStateWithHeatLoss]:
        neighbours = []
        direction = item.direction

        if direction is None:
            # currently at start - pretend direction is down (down or right would work)
            direction = Direction.RIGHTWARDS

        offsets = OFFSETS[direction]

        for offset_coord, offset_dir in offsets:
            if direction == offset_dir:
                if item.straight_steps == self.max_consec_steps:
                    continue
                step_change = 1
                offset_straight_steps = item.straight_steps + step_change
            else:
                step_change = self.min_consec_steps
                offset_straight_steps = step_change

            traversal_results = self._traverse_city(
                start=item.location, offset=offset_coord, step_change=step_change
            )
            if traversal_results is None:
                continue
            neighbour_coord, heat_loss = traversal_results

            neighbours.append(
                LocationStateWithHeatLoss(
                    heat_loss=heat_loss,
                    location=neighbour_coord,
                    direction=offset_dir,
                    straight_steps=offset_straight_steps,
                )
            )
        return neighbours

    def _process_next_state(self) -> int | None:
        item: LocationStateWithHeatLoss = heapq.heappop(self.q)
        if item.location == self.end:
            return item.heat_loss

        current_visited_state = LocationState(
            location=item.location,
            direction=item.direction,
            straight_steps=item.straight_steps,
        )
        if current_visited_state in self.visited:
            return None

        for steps in range(item.straight_steps, self.max_consec_steps + 1):
            self.visited.add(
                LocationState(
                    location=item.location,
                    direction=item.direction,
                    straight_steps=steps,
                )
            )

        for neighbour_visited_state in self._get_neighbours(item):
            if neighbour_visited_state in self.visited:
                continue

            state = LocationState(
                location=neighbour_visited_state.location,
                direction=neighbour_visited_state.direction,
                straight_steps=neighbour_visited_state.straight_steps,
            )

            old_cost = self.costs.get(state)
            new_cost = (
                self.costs.get(current_visited_state)
                + neighbour_visited_state.heat_loss
            )
            if old_cost is not None and new_cost >= old_cost:
                continue

            heapq.heappush(
                self.q,
                LocationStateWithHeatLoss(
                    heat_loss=new_cost,
                    location=neighbour_visited_state.location,
                    direction=neighbour_visited_state.direction,
                    straight_steps=neighbour_visited_state.straight_steps,
                ),
            )
            self.costs[state] = new_cost

        return None

    def minimise_heat_loss(self):
        while self.q:
            result = self._process_next_state()
            if result is not None:
                return result


def crucible_minimal_heat_loss(city):
    heat_loss_minimiser = _HeatLossMinimiser(
        city=city, min_consec_steps=1, max_consec_steps=3
    )
    return heat_loss_minimiser.minimise_heat_loss()


def ultra_crucible_minimal_heat_loss(city):
    heat_loss_minimiser = _HeatLossMinimiser(
        city=city, min_consec_steps=4, max_consec_steps=10
    )
    return heat_loss_minimiser.minimise_heat_loss()


def main() -> None:
    city = City.read_file()
    print(
        "Least heat loss incurred by crucible directed from lava pool to machine parts factory:",
        crucible_minimal_heat_loss(city),
    )
    print(
        "Least heat loss incurred by ultra crucible directed from lava pool to machine parts factory:",
        ultra_crucible_minimal_heat_loss(city),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
