import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Race:
    time: int
    winning_dist: int


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

        self.races = list(Race(*race_detail) for race_detail in zip(times, dists))

    def distances(self) -> list[list[int]]:
        distances = []
        for race in self.races:
            race_dists = []
            for hold_time in range(race.time + 1):
                release_time = race.time - hold_time
                race_dist = hold_time * release_time
                race_dists.append(race_dist)
            distances.append(race_dists)
        return distances


def read_file() -> str:
    with open("input.txt") as f:
        return f.read().strip()


def num_of_winning_distances(races: Races) -> list[int]:
    winning_distances = []
    for race, distances in zip(races.races, races.distances()):
        race_winning_distances = [dist for dist in distances if dist > race.winning_dist]
        winning_distances.append(len(race_winning_distances))
    return winning_distances


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
