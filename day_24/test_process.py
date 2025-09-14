from day_24 import process


def test_parse_step_example_1():
    assert process.LobbyLayout.parse_step('esenee') == ['e', 'se', 'ne', 'e']


def test_parse_step_example_2():
    input_ = 'sesenwnenenewseeswwswswwnenewsewsw'
    expected = ['se', 'se', 'nw', 'ne', 'ne', 'ne', 'w', 'se', 'e', 'sw', 'w', 'sw', 'sw', 'w', 'ne', 'ne', 'w', 'se', 'w', 'sw']
    assert process.LobbyLayout.parse_step(input_) == expected


def test_position_change():
    assert process.LobbyLayout._calculate_position(['e', 'se', 'w']) == process.Coords(1, -2)


def test_position_change_2():
    assert process.LobbyLayout._calculate_position(['nw', 'w', 'sw', 'e', 'e']) == process.Coords(0, 0)


def test_steps_example():
    input_ = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""
    lobby_layout = process.LobbyLayout(input_)
    lobby_layout.process_steps()
    assert lobby_layout.black_tiles == 10


def test_steps_example_flip():
    input_ = """\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""
    lobby_layout = process.LobbyLayout(input_)
    lobby_layout.process_steps()
    assert lobby_layout.black_tiles == 10
    iter_flip = lobby_layout.flip(until_day=100)

    assert next(iter_flip) == 15
    assert next(iter_flip) == 12
    assert next(iter_flip) == 25
    assert next(iter_flip) == 14
    assert next(iter_flip) == 23
    assert next(iter_flip) == 28
    assert next(iter_flip) == 41
    assert next(iter_flip) == 37
    assert next(iter_flip) == 49
    assert next(iter_flip) == 37

    for _ in range(9):
        next(iter_flip)
    assert next(iter_flip) == 132

    for _ in range(9):
        next(iter_flip)
    assert next(iter_flip) == 259

    for _ in range(9):
        next(iter_flip)
    assert next(iter_flip) == 406

    for _ in range(9):
        next(iter_flip)
    assert next(iter_flip) == 566

    for _ in range(9):
        next(iter_flip)
    assert next(iter_flip) == 788

    for _ in range(9):
        next(iter_flip)
    assert next(iter_flip) == 1106

    for _ in range(9):
        next(iter_flip)
    assert next(iter_flip) == 1373

    for _ in range(9):
        next(iter_flip)
    assert next(iter_flip) == 1844

    for _ in range(9):
        next(iter_flip)
    assert next(iter_flip) == 2208
