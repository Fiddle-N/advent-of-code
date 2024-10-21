import itertools
import re
from enum import Enum, auto
from dataclasses import dataclass
from functools import cache
from typing import Optional, Self


FILENAME = 'input.txt'


@dataclass(frozen=True)
class Coord:
    x: float
    y: float


class PathOutcome(Enum):
    PARALLEL = auto()
    CROSSED_INSIDE_AREA = auto()
    CROSSED_OUTSIDE_AREA = auto()
    CROSSED_IN_PAST_FOR_A = auto()
    CROSSED_IN_PAST_FOR_B = auto()
    CROSSED_IN_PAST_FOR_BOTH = auto()


@dataclass(frozen=True)
class VecCmpnt:
    pos: int
    vel: int

    @cache
    def rate_of_change(self: Self) -> float:
        return 1 / self.vel

    @cache
    def constant(self: Self) -> float:
        return -(self.pos) / self.vel
    
    @cache
    def time(self: Self, pos: float) -> float:
        return self.rate_of_change() * pos + self.constant()


@dataclass(frozen=True)
class Vec:
    x: VecCmpnt
    y: VecCmpnt
    z: VecCmpnt

    @cache
    def constant_2d(self: Self) -> float:
        return (self.y.constant() - self.x.constant()) / -self.y.rate_of_change()
    
    @cache
    def gradient_2d(self: Self) -> float:
        return -(self.x.rate_of_change()) / -self.y.rate_of_change()
    
    @cache
    def time_x(self: Self, pos: float) -> float:
        return self.x.time(pos)

    @cache
    def time_y(self: Self, pos: float) -> float:
        return self.x.time(pos)


def intercept_2d(a: Vec, b: Vec) -> Optional[Coord]:
    gradient = b.gradient_2d() - a.gradient_2d()
    if gradient == 0:
        return None
    x = (a.constant_2d() - b.constant_2d()) / gradient
    y = (a.gradient_2d() * x) + a.constant_2d()
    return Coord(x, y)


def calculate_crossing_2d(a: Vec, b: Vec, min_: int, max_: int) -> tuple[PathOutcome, Optional[Coord]]:
    intercept = intercept_2d(a, b)
    if intercept is None:
        return (PathOutcome.PARALLEL, None)
    a_time = a.time_x(intercept.x)    
    b_time = b.time_x(intercept.x)    
    if a_time < 0 and b_time < 0:
        return (PathOutcome.CROSSED_IN_PAST_FOR_BOTH, None)
    if a_time < 0:
        return (PathOutcome.CROSSED_IN_PAST_FOR_A, None)
    if b_time < 0:
        return (PathOutcome.CROSSED_IN_PAST_FOR_B, None)
    if not (
        (min_ <= intercept.x <= max_) 
        and (min_ <= intercept.y <= max_)
    ):
        return (PathOutcome.CROSSED_OUTSIDE_AREA, intercept)
    return (PathOutcome.CROSSED_INSIDE_AREA, intercept)


def sum_intersecting_vecs_2d(vecs: list[Vec], min_: int, max_: int) -> int:
    results: list[bool] = []
    for a, b in itertools.combinations(vecs, 2):
        result = calculate_crossing_2d(a, b, min_, max_)
        results.append(result[0] == PathOutcome.CROSSED_INSIDE_AREA)
    return sum(results)


def parse_vectors(vec_text: str) -> list[Vec]:
    vecs = []
    for vec_str in vec_text.splitlines():
        vec_vals: list[str] = re.findall(r"-?\d+", vec_str)
        vecs.append(Vec(
            VecCmpnt(int(vec_vals[0]), int(vec_vals[3])),
            VecCmpnt(int(vec_vals[1]), int(vec_vals[4])),
            VecCmpnt(int(vec_vals[2]), int(vec_vals[5])),
        ))
    return vecs


def read_file() -> str:
    with open(FILENAME) as f:
        return f.read()


def main():
    vec_text = read_file()
    vecs = parse_vectors(vec_text)
    print(
        "Intersecting vectors within test area 2D:",
        sum_intersecting_vecs_2d(vecs, min_=200000000000000, max_=400000000000000)
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))

