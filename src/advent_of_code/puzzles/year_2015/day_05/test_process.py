import pytest

from advent_of_code.puzzles.year_2015.day_05 import process


@pytest.mark.parametrize(
    "str_,is_nice",
    [
        ("aei", True),
        ("xazegov", True),
        ("aeiouaeiouaeiou", True),
        ("aew", False),  # only two vowels
    ],
)
def test_contains_three_vowels(str_: str, is_nice: bool) -> None:
    assert process._contains_three_vowels(str_) == is_nice


@pytest.mark.parametrize(
    "str_,is_nice",
    [
        ("xx", True),
        ("abcdde", True),
        ("aabbccdd", True),
        ("abcde", False),
    ],
)
def test_contains_one_letter_twice_in_a_row(str_: str, is_nice: bool) -> None:
    assert process._contains_one_letter_twice_in_a_row(str_) == is_nice


@pytest.mark.parametrize(
    "str_,is_nice",
    [
        ("a", False),
        ("aa", False),
        ("aaa", False),
        ("aaaa", True),
        ("xyxy", True),
        ("aabcdefgaa", True),
    ],
)
def test_contains_char_pair_twice_nonoverlapping(str_: str, is_nice: bool) -> None:
    assert process._contains_char_pair_twice_nonoverlapping(str_) == is_nice


@pytest.mark.parametrize(
    "str_,is_nice",
    [
        ("xyx", True),
        ("xyz", False),
        ("abcdefeghi", True),
        ("aaa", True),
    ],
)
def test_contains_one_letter_repeating_with_exactly_one_letter_between(
    str_: str, is_nice: bool
) -> None:
    assert (
        process._contains_one_letter_repeating_with_exactly_one_letter_between(str_)
        == is_nice
    )


@pytest.mark.parametrize(
    "str_,is_nice",
    [
        ("ugknbfddgicrmopn", True),
        ("aaa", True),
        ("jchzalrnumimnmhp", False),
        ("haegwjzuvuyypxyu", False),
        ("dvszwmarrgswjxmb", False),
    ],
)
def test_is_nice(str_: str, is_nice: bool) -> None:
    assert process.is_nice(str_) == is_nice


@pytest.mark.parametrize(
    "str_,is_nice",
    [
        ("qjhvhtzxzqqjkmpb", True),
        ("xxyxx", True),
        ("uurcxstgmygtbstg", False),
        ("ieodomkazucvgmuy", False),
    ],
)
def test_is_nice_v2(str_: str, is_nice: bool) -> None:
    assert process.is_nice_v2(str_) == is_nice
