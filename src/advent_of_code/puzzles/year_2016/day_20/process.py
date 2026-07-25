from itertools import pairwise

from advent_of_code.common import merge_intervals, read_file, timed_run

MIN_VAL = 0
MAX_VAL = 4294967295


def parse_intervals(raw_intervals: str) -> list[tuple[int, int]]:
    intervals = []
    for raw_interval in raw_intervals.splitlines():
        min_, max_ = raw_interval.split("-")
        intervals.append((int(min_), int(max_)))
    return intervals


def lowest_valid_ip(intervals: list[tuple[int, int]]) -> int:
    # assumes intervals are sorted and merged
    return intervals[0][1] + 1


def allowed_ips(intervals: list[tuple[int, int]]) -> int:
    allowed = 0
    # capture allowed below min blocked range
    if intervals[0][0] > MIN_VAL:
        allowed += intervals[0][0] - MIN_VAL

    for l_interval, r_interval in pairwise(intervals):
        allowed += r_interval[0] - l_interval[1] - 1

    if intervals[-1][-1] < MAX_VAL:
        allowed += MAX_VAL - intervals[-1][-1]

    return allowed


def run():
    raw_intervals = read_file()
    intervals = parse_intervals(raw_intervals)
    merged_intervals = merge_intervals(intervals)
    print(lowest_valid_ip(merged_intervals))
    print(allowed_ips(merged_intervals))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
