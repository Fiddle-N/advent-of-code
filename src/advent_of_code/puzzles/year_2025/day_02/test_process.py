from advent_of_code.puzzles.year_2025.day_02 import process


def test_check_id_range_two_repetitions():
    id_ranges = process.parse("""\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124""")
    assert process.check_id_range_two_repetitions(id_ranges) == 1227775554


def test_check_id_range_any_repetitions():
    id_ranges = process.parse("""\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124""")
    assert process.check_id_range_any_repetitions(id_ranges) == 4174379265
