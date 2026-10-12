from advent_of_code.puzzles.year_2018.day_04 import process


def test_calculate_sleepiest_strategy() -> None:
    raw_log = """\
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""
    sleep_record = process.parse_to_record(raw_log)
    assert process.calculate_sleepiest_strategy(sleep_record) == (240, 4455)


def test_calculate_sleepiest_strategy_unordered_log() -> None:
    raw_log = """\
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-01 00:25] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-03 00:29] wakes up
[1518-11-02 00:40] falls asleep
[1518-11-05 00:45] falls asleep
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-01 00:30] falls asleep
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-01 00:55] wakes up
[1518-11-05 00:55] wakes up"""
    sleep_record = process.parse_to_record(raw_log)
    assert process.calculate_sleepiest_strategy(sleep_record) == (240, 4455)
