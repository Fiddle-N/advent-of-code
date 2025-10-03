import re
from collections import Counter
from dataclasses import dataclass

from advent_of_code.common import read_file, timed_run

RACE_TIME = 2503

STAT_PATTERN = r"(?P<name>\w+) can fly (?P<speed>\d+) km/s for (?P<duration>\d+) seconds, but then must rest for (?P<rest>\d+) seconds."


@dataclass(frozen=True)
class ReindeerStats:
    name: str
    speed: int
    duration: int
    rest: int

    def calculate_distance(self, time: int) -> int:
        time_period = self.duration + self.rest
        elapsed_periods, extra_time = divmod(time, time_period)
        extra_flying_time = extra_time if extra_time <= self.duration else self.duration
        distance = (elapsed_periods * self.duration * self.speed) + (
            extra_flying_time * self.speed
        )
        return distance


def parse_stats(stat_text: str) -> list[ReindeerStats]:
    reindeers: list[ReindeerStats] = []
    for line in stat_text.splitlines():
        if (match := re.fullmatch(STAT_PATTERN, line)) is not None:
            name = match.group("name")
            speed = int(match.group("speed"))
            duration = int(match.group("duration"))
            rest = int(match.group("rest"))
            reindeers.append(ReindeerStats(name, speed, duration, rest))
    return reindeers


def calculate_longest_distance(reindeer_stats: list[ReindeerStats], time: int) -> int:
    longest_distance = 0
    for reindeer in reindeer_stats:
        distance = reindeer.calculate_distance(time)
        if distance > longest_distance:
            longest_distance = distance
    return longest_distance


def calculate_max_score(reindeer_stats: list[ReindeerStats], time: int) -> int:
    cum_scores = Counter()
    for seconds in range(1, time + 1):
        scores = {
            reindeer.name: reindeer.calculate_distance(seconds)
            for reindeer in reindeer_stats
        }
        max_score = max(scores.values())
        winners = [name for name, score in scores.items() if score == max_score]
        for winner in winners:
            cum_scores[winner] += 1
    return cum_scores.most_common(1)[0][1]


def run():
    reindeer_text = read_file()
    reindeer_stats = parse_stats(reindeer_text)
    print(calculate_longest_distance(reindeer_stats, RACE_TIME))
    print(calculate_max_score(reindeer_stats, RACE_TIME))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
