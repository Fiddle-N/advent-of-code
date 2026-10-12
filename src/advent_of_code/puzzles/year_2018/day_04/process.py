import operator
import re
from collections import defaultdict, Counter
from datetime import datetime

from advent_of_code.common import read_file, timed_run

LOG_PATTERN = r"\[(?P<timestamp>.+)\] (?P<entry>.+)"
TIMESTAMP_PATTERN = "%Y-%m-%d %H:%M"
GUARD_PATTERN = r"Guard #(?P<guard>\d+) begins shift"


def _sort_log(raw_log: str) -> list[tuple[datetime, str]]:
    timestamped_log = []
    for log_line in raw_log.splitlines():
        match = re.fullmatch(LOG_PATTERN, log_line)
        assert match is not None
        timestamp = datetime.strptime(match["timestamp"], "%Y-%m-%d %H:%M")
        timestamped_log.append((timestamp, match["entry"]))
    return sorted(timestamped_log, key=operator.itemgetter(0))


def _transform_to_record(
    sorted_log: list[tuple[datetime, str]],
) -> dict[int, list[set[int]]]:
    sleep_record = defaultdict(list)

    current_guard = None
    start_min = None
    end_min = None

    for timestamp, entry in sorted_log:
        if (match := re.fullmatch(GUARD_PATTERN, entry)) is not None:
            current_guard = int(match["guard"])
        elif entry == "falls asleep":
            start_min = timestamp.minute
        elif entry == "wakes up":
            end_min = timestamp.minute
        else:
            raise ValueError("invalid entry")
        if start_min is not None and end_min is not None:
            sleep_record[current_guard].append(set(range(start_min, end_min)))
            start_min = None
            end_min = None

    return dict(sleep_record)


def calculate_sleepiest_strategy(
    sleep_record: dict[int, list[set[int]]],
) -> tuple[int, int]:
    minutes_asleep = Counter(
        {
            guard: sum(len(asleep_range) for asleep_range in asleep_ranges)
            for guard, asleep_ranges in sleep_record.items()
        }
    )

    minutes_asleep_count = {}
    for guard, asleep_ranges in sleep_record.items():
        count = Counter()
        for asleep_range in asleep_ranges:
            count.update(asleep_range)
        minutes_asleep_count[guard] = count

    sleepiest_guard = minutes_asleep.most_common(1)[0][0]
    sleepiest_guard_sleepiest_minute = minutes_asleep_count[
        sleepiest_guard
    ].most_common(1)[0][0]

    guards_sleepiest_minute = {
        guard: count.most_common(1)[0] for guard, count in minutes_asleep_count.items()
    }

    (sleepiest_minute_guard, (sleepiest_minute, _)) = max(
        guards_sleepiest_minute.items(), key=lambda sleepiest_min: sleepiest_min[1][1]
    )

    return (sleepiest_guard * sleepiest_guard_sleepiest_minute), (
        sleepiest_minute_guard * sleepiest_minute
    )


def parse_to_record(raw_log: str):
    sorted_log = _sort_log(raw_log)
    sleep_record = _transform_to_record(sorted_log)
    return sleep_record


def run():
    raw_log = read_file()
    sleep_record = parse_to_record(raw_log)
    print(calculate_sleepiest_strategy(sleep_record))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
