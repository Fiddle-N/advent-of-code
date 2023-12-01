from year_2023.day_01 import process


def test_example_without_word_numbers():
    assert process.sum_cal_vals("""\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""", include_word_numbers=False) == 142


def test_example_with_word_numbers():
    assert process.sum_cal_vals("""\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""", include_word_numbers=True) == 281


def test_example_with_overlapping_matches_counts_overlapped_numbers():
    """
    Apparently even though number words count as "digits"
    they can be reused for multiple numbers
    so include overlapped matches
    """
    assert process.sum_cal_vals("""\
eightoneight""", include_word_numbers=True) == 88
