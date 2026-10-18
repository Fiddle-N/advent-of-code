from dataclasses import dataclass
from typing import Literal
from re import fullmatch

from advent_of_code.common import BaseCoords, read_file, timed_run


POINT_PATTERN = r"position=<(?P<position_x>.*), (?P<position_y>.*)> velocity=<(?P<velocity_x>.*), (?P<velocity_y>.*)>"

Position = BaseCoords
Velocity = BaseCoords


@dataclass
class Point:
    position: Position
    velocity: Velocity


class Points(list[Point]):
    _POINT = "#"
    _SPACE = "."
    _P_POINT = "██"
    _P_SPACE = "  "

    _BOUNDARY_FNS = {"min": min, "max": max}

    def _get_boundary_val(
        self, boundary: Literal["min", "max"], axis: Literal["x", "y"]
    ) -> int:
        boundary_fn = self._BOUNDARY_FNS[boundary]
        return getattr(
            boundary_fn(self, key=lambda point: getattr(point.position, axis)).position,
            axis,
        )

    @property
    def min_position_x(self) -> int:
        return self._get_boundary_val("min", "x")

    @property
    def max_position_x(self) -> int:
        return self._get_boundary_val("max", "x")

    @property
    def min_position_y(self) -> int:
        return self._get_boundary_val("min", "y")

    @property
    def max_position_y(self) -> int:
        return self._get_boundary_val("max", "y")

    @property
    def area(self) -> int:
        return (self.max_position_x - self.min_position_x) * (
            self.max_position_y - self.min_position_y
        )

    def _render(self, point_px: str, space_px: str) -> str:
        positions = {point.position for point in self}
        return "\n".join(
            "".join(
                [
                    point_px if Position(x, y) in positions else space_px
                    for x in range(self.min_position_x, self.max_position_x + 1)
                ]
            )
            for y in range(self.min_position_y, self.max_position_y + 1)
        )

    def __str__(self) -> str:
        return self._render(self._POINT, self._SPACE)

    def render(self) -> str:
        return self._render(self._P_POINT, self._P_SPACE)


def parse_points(raw_points: str) -> Points:
    points = Points()
    for raw_point in raw_points.splitlines():
        point_match = fullmatch(POINT_PATTERN, raw_point)
        assert point_match
        position = Position(
            int(point_match["position_x"]), int(point_match["position_y"])
        )
        velocity = Velocity(
            int(point_match["velocity_x"]), int(point_match["velocity_y"])
        )
        points.append(Point(position, velocity))
    return points


def align_points(points: Points) -> tuple[Points, int]:
    seconds = 0
    while True:
        next_points = Points()
        for point in points:
            next_position = point.position + point.velocity
            next_points.append(Point(position=next_position, velocity=point.velocity))
        if next_points.area > points.area:
            return points, seconds
        points = next_points
        seconds += 1


def run() -> None:
    raw_points = read_file()
    points = parse_points(raw_points)
    message_points, seconds_taken = align_points(points)
    print(message_points.render())
    print(seconds_taken)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
