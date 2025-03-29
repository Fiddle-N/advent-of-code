from advent_of_code.year_2023.day_18 import process


def test_1():
    input_ = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
    plan = process.parse_plan(input_)
    assert plan == [
        process.DigInstruct(process.Direction.RIGHT, num=6),
        process.DigInstruct(process.Direction.DOWN, num=5),
        process.DigInstruct(process.Direction.LEFT, num=2),
        process.DigInstruct(process.Direction.DOWN, num=2),
        process.DigInstruct(process.Direction.RIGHT, num=2),
        process.DigInstruct(process.Direction.DOWN, num=2),
        process.DigInstruct(process.Direction.LEFT, num=5),
        process.DigInstruct(process.Direction.UP, num=2),
        process.DigInstruct(process.Direction.LEFT, num=1),
        process.DigInstruct(process.Direction.UP, num=2),
        process.DigInstruct(process.Direction.RIGHT, num=2),
        process.DigInstruct(process.Direction.UP, num=3),
        process.DigInstruct(process.Direction.LEFT, num=2),
        process.DigInstruct(process.Direction.UP, num=2),
    ]
    assert process.capacity(plan) == 62


def test_2():
    input_ = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
    plan = process.parse_plan(input_, extract_data_from_hex=True)
    assert plan == [
        process.DigInstruct(process.Direction.RIGHT, num=461937),
        process.DigInstruct(process.Direction.DOWN, num=56407),
        process.DigInstruct(process.Direction.RIGHT, num=356671),
        process.DigInstruct(process.Direction.DOWN, num=863240),
        process.DigInstruct(process.Direction.RIGHT, num=367720),
        process.DigInstruct(process.Direction.DOWN, num=266681),
        process.DigInstruct(process.Direction.LEFT, num=577262),
        process.DigInstruct(process.Direction.UP, num=829975),
        process.DigInstruct(process.Direction.LEFT, num=112010),
        process.DigInstruct(process.Direction.DOWN, num=829975),
        process.DigInstruct(process.Direction.LEFT, num=491645),
        process.DigInstruct(process.Direction.UP, num=686074),
        process.DigInstruct(process.Direction.LEFT, num=5411),
        process.DigInstruct(process.Direction.UP, num=500254),
    ]
    assert process.capacity(plan) == 952408144115
