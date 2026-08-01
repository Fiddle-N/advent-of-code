import pytest


from advent_of_code.puzzles.year_2017.day_09 import process


@pytest.mark.parametrize(
    "group_text,score",
    [
        ("{}", 1),
        ("{{{}}}", 6),
        ("{{},{}}", 5),
        ("{{{},{},{{}}}}", 16),
        ("{<a>,<a>,<a>,<a>}", 1),
        ("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9),
        ("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9),
        ("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3),
    ],
)
def test_calculate_score(group_text: str, score: int) -> None:
    group = process.stream_parser.parse(group_text)
    assert process.calculate_score(group) == score


@pytest.mark.parametrize(
    "group_text,chars",
    [
        ("{<>}", 0),
        ("{<random characters>}", 17),
        ("{<<<<>}", 3),
        ("{<{!>}>}", 2),
        ("{<!!>}", 0),
        ("{<!!!>>}", 0),
        ('{<{o"i!a,<{i<a>}', 10),
    ],
)
def test_count_garbage(group_text: str, chars: int) -> None:
    group = process.stream_parser.parse(group_text)
    assert process.count_garbage(group) == chars
