import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Race:
    time: int
    winning_dist: int


@dataclass(frozen=True)
class WinningRange:
    hold_at_least: int
    hold_at_most: int

    def __len__(self):
        return self.hold_at_most - self.hold_at_least + 1


def quad_formula(a, b, c):
    sqrt_b2_4ac = (b ** 2 - 4 * a * c) ** 0.5
    denominator_2a = 2 * a
    plus_case = (-b + sqrt_b2_4ac) / denominator_2a
    minus_case = (-b - sqrt_b2_4ac) / denominator_2a
    return plus_case, minus_case


class Races:

    def __init__(self, race_input: str, long_race=False) -> None:
        race_info = race_input.splitlines()

        time_info = race_info[0]
        time_label, *times = time_info.strip().split()
        assert time_label == 'Time:'
        times = (
            [int(''.join(times))]
            if long_race
            else [int(time) for time in times]
        )

        dist_info = race_info[1]
        dist_label, *dists = dist_info.strip().split()
        assert dist_label == 'Distance:'
        dists = (
            [int(''.join(dists))]
            if long_race
            else [int(dist) for dist in dists]
        )

        self.races = [Race(*race_detail) for race_detail in zip(times, dists)]

    def winning_ranges(self) -> list[WinningRange]:
        winning_ranges = []
        for race in self.races:
            # apply quadratic formula
            # if time to hold the button is x, race time is y and distance record is z
            # then the race equation can be defined as x(y - x) > z
            # we can plug in y and z; so if time is 7 and distance is 9 the equation is x(7 - x) > 9
            # this expands to x^2 - 7x + 9 < 0
            # a quadratic equation - we need to solve for x^2 - 7x + 9 = 0, which will have two solutions
            # x can be found by the quadratic formula: (-b +- sqrt(b^2 - 4ac)) / 2a
            # where a = 1, b = -7 and c = 9
            # then find all integer solutions in the range between the two bounds

            a = 1
            b = -race.time
            c = race.winning_dist
            upper_bound, lower_bound = quad_formula(a, b, c)

            # the least time to hold is always the nearest integer higher than the lower bound
            # e.g.
            # least time to hold is 11 if lower bound is 10 to 10.999...
            # but 12 if lower bound is exactly 11
            hold_at_least = math.floor(lower_bound) + 1

            # the most time to hold is always the nearest integer lower than the upper bound
            # e.g.
            # most time to hold is 10 if upper bound is 10.000...1 to 11
            # but 9 if upper bound is exactly 10
            hold_at_most = math.ceil(upper_bound) - 1

            winning_ranges.append(WinningRange(hold_at_least, hold_at_most))

        return winning_ranges


def read_file() -> str:
    with open("input.txt") as f:
        return f.read().strip()


def num_of_winning_distances(races: Races) -> list[int]:
    winning_distances_nums = [
        len(winning_range)
        for winning_range in races.winning_ranges()
    ]
    return winning_distances_nums


def main() -> None:
    races_info = read_file()
    races = Races(races_info)
    print(
        f"Number of ways to beat the record for all races, multiplied together:",
        math.prod(num_of_winning_distances(races)),
    )
    long_race = Races(races_info, long_race=True)
    print(
        f"Number of ways to beat the record for long race, multiplied together:",
        math.prod(num_of_winning_distances(long_race)),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
