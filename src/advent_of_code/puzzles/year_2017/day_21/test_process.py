from advent_of_code.puzzles.year_2017.day_21 import process


def test_example():
    raw_transformations = """\
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""
    transformations = process.parse(raw_transformations)
    result = process.enhance(transformations, n=2)
    on_pixels = process.count_on_pixels(result)
    assert on_pixels == 12
