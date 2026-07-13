from advent_of_code.puzzles.year_2016.day_06 import process


def test_err_correct():
    assert process.err_correct("""\
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar""") == ("easter", "advent")
