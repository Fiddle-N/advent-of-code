from advent_of_code.puzzles.year_2018.day_02 import process


def test_calculate_checksum() -> None:
    ids = """\
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab""".splitlines()
    assert process.calculate_checksum(ids) == 12


def test_get_correct_ids_common_letters() -> None:
    ids = """\
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz""".splitlines()
    assert process.get_correct_ids_common_letters(ids) == "fgij"
