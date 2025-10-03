from advent_of_code.puzzles.year_2015.day_14 import process


def test_calculate_longest_distance() -> None:
    reindeer_text = """\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""
    reindeer_stats = process.parse_stats(reindeer_text)
    assert process.calculate_longest_distance(reindeer_stats, time=1000) == 1120


def test_calculate_max_score() -> None:
    reindeer_text = """\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""
    reindeer_stats = process.parse_stats(reindeer_text)
    assert process.calculate_max_score(reindeer_stats, time=1000) == 689
