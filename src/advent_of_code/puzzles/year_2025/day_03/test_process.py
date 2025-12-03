from advent_of_code.puzzles.year_2025.day_03 import process


def test_find_max_joltage_two_digits():
    banks = process.parse("""\
987654321111111
811111111111119
234234234234278
818181911112111""")
    assert process.find_max_joltage(banks, digits=2) == 357


def test_find_max_joltage_twelve_digits():
    banks = process.parse("""\
987654321111111
811111111111119
234234234234278
818181911112111""")
    assert process.find_max_joltage(banks, digits=12) == 3121910778619
