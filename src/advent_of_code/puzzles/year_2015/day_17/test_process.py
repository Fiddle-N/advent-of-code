from advent_of_code.puzzles.year_2015.day_17 import process


def test_eggnog_resolver() -> None:
    container_text = """\
20
15
10
5
5"""
    containers = process.parse_containers(container_text)
    assert process.EggnogResolver().resolve(containers, target=25) == (4, 3)
