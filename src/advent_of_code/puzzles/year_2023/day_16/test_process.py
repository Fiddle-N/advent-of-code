from advent_of_code.puzzles.year_2023.day_16 import process


def test_contraption_beam_from_top_left_corner():
    contraption_input = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
    contraption = process.Contraption(contraption_input)
    energised_spaces = contraption.simulate_beam()
    assert energised_spaces == {
        process.Coords(0, 0): {process.Direction.RIGHTWARDS},
        process.Coords(1, 0): {process.Direction.UPWARDS, process.Direction.DOWNWARDS},
        process.Coords(2, 0): {process.Direction.LEFTWARDS},
        process.Coords(3, 0): {process.Direction.LEFTWARDS},
        process.Coords(4, 0): {process.Direction.LEFTWARDS},
        process.Coords(5, 0): {process.Direction.LEFTWARDS},
        process.Coords(1, 1): {process.Direction.DOWNWARDS},
        process.Coords(5, 1): {process.Direction.UPWARDS},
        process.Coords(1, 2): {process.Direction.DOWNWARDS},
        process.Coords(5, 2): {process.Direction.UPWARDS, process.Direction.DOWNWARDS},
        process.Coords(6, 2): {
            process.Direction.LEFTWARDS,
            process.Direction.RIGHTWARDS,
        },
        process.Coords(7, 2): {process.Direction.RIGHTWARDS},
        process.Coords(8, 2): {process.Direction.RIGHTWARDS},
        process.Coords(9, 2): {process.Direction.RIGHTWARDS},
        process.Coords(1, 3): {process.Direction.DOWNWARDS},
        process.Coords(5, 3): {process.Direction.DOWNWARDS},
        process.Coords(6, 3): {process.Direction.UPWARDS},
        process.Coords(1, 4): {process.Direction.DOWNWARDS},
        process.Coords(5, 4): {process.Direction.DOWNWARDS},
        process.Coords(6, 4): {process.Direction.UPWARDS},
        process.Coords(1, 5): {process.Direction.DOWNWARDS},
        process.Coords(5, 5): {process.Direction.DOWNWARDS},
        process.Coords(6, 5): {process.Direction.UPWARDS},
        process.Coords(1, 6): {process.Direction.DOWNWARDS},
        process.Coords(4, 6): {process.Direction.RIGHTWARDS},
        process.Coords(5, 6): {
            process.Direction.DOWNWARDS,
            process.Direction.RIGHTWARDS,
        },
        process.Coords(6, 6): {process.Direction.UPWARDS, process.Direction.DOWNWARDS},
        process.Coords(7, 6): {process.Direction.LEFTWARDS},
        process.Coords(0, 7): {process.Direction.LEFTWARDS},
        process.Coords(1, 7): {
            process.Direction.LEFTWARDS,
            process.Direction.RIGHTWARDS,
        },
        process.Coords(2, 7): {process.Direction.RIGHTWARDS},
        process.Coords(3, 7): {process.Direction.RIGHTWARDS},
        process.Coords(4, 7): {process.Direction.UPWARDS},
        process.Coords(5, 7): {process.Direction.DOWNWARDS},
        process.Coords(6, 7): {process.Direction.DOWNWARDS},
        process.Coords(7, 7): {process.Direction.UPWARDS},
        process.Coords(1, 8): {process.Direction.UPWARDS, process.Direction.DOWNWARDS},
        process.Coords(2, 8): {process.Direction.LEFTWARDS},
        process.Coords(3, 8): {process.Direction.LEFTWARDS},
        process.Coords(4, 8): {process.Direction.LEFTWARDS},
        process.Coords(5, 8): {
            process.Direction.LEFTWARDS,
            process.Direction.DOWNWARDS,
        },
        process.Coords(6, 8): {
            process.Direction.LEFTWARDS,
            process.Direction.RIGHTWARDS,
        },
        process.Coords(7, 8): {process.Direction.UPWARDS, process.Direction.DOWNWARDS},
        process.Coords(1, 9): {process.Direction.DOWNWARDS},
        process.Coords(5, 9): {process.Direction.DOWNWARDS},
        process.Coords(7, 9): {process.Direction.DOWNWARDS},
    }
    assert len(energised_spaces) == 46


def test_contraption_best_energised_spaces():
    contraption_input = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
    contraption = process.Contraption(contraption_input)
    best_config = contraption.best_configuration()
    best_energised_spaces, best_tile_num = best_config
    assert best_energised_spaces == {
        process.Coords(1, 0): {process.Direction.UPWARDS, process.Direction.DOWNWARDS},
        process.Coords(2, 0): {process.Direction.LEFTWARDS},
        process.Coords(3, 0): {
            process.Direction.LEFTWARDS,
            process.Direction.DOWNWARDS,
        },
        process.Coords(4, 0): {process.Direction.LEFTWARDS},
        process.Coords(5, 0): {process.Direction.LEFTWARDS},
        process.Coords(1, 1): {process.Direction.DOWNWARDS},
        process.Coords(3, 1): {process.Direction.DOWNWARDS},
        process.Coords(5, 1): {process.Direction.UPWARDS},
        process.Coords(1, 2): {process.Direction.DOWNWARDS},
        process.Coords(3, 2): {process.Direction.DOWNWARDS},
        process.Coords(5, 2): {process.Direction.UPWARDS, process.Direction.DOWNWARDS},
        process.Coords(6, 2): {
            process.Direction.LEFTWARDS,
            process.Direction.RIGHTWARDS,
        },
        process.Coords(7, 2): {process.Direction.RIGHTWARDS},
        process.Coords(8, 2): {process.Direction.RIGHTWARDS},
        process.Coords(9, 2): {process.Direction.RIGHTWARDS},
        process.Coords(1, 3): {process.Direction.DOWNWARDS},
        process.Coords(3, 3): {process.Direction.DOWNWARDS},
        process.Coords(5, 3): {process.Direction.DOWNWARDS},
        process.Coords(6, 3): {process.Direction.UPWARDS},
        process.Coords(1, 4): {process.Direction.DOWNWARDS},
        process.Coords(3, 4): {process.Direction.DOWNWARDS},
        process.Coords(5, 4): {process.Direction.DOWNWARDS},
        process.Coords(6, 4): {process.Direction.UPWARDS},
        process.Coords(1, 5): {process.Direction.DOWNWARDS},
        process.Coords(3, 5): {process.Direction.DOWNWARDS},
        process.Coords(5, 5): {process.Direction.DOWNWARDS},
        process.Coords(6, 5): {process.Direction.UPWARDS},
        process.Coords(1, 6): {process.Direction.DOWNWARDS},
        process.Coords(3, 6): {process.Direction.DOWNWARDS},
        process.Coords(4, 6): {process.Direction.RIGHTWARDS},
        process.Coords(5, 6): {
            process.Direction.RIGHTWARDS,
            process.Direction.DOWNWARDS,
        },
        process.Coords(6, 6): {process.Direction.UPWARDS, process.Direction.DOWNWARDS},
        process.Coords(7, 6): {process.Direction.LEFTWARDS},
        process.Coords(0, 7): {process.Direction.LEFTWARDS},
        process.Coords(1, 7): {
            process.Direction.LEFTWARDS,
            process.Direction.RIGHTWARDS,
        },
        process.Coords(2, 7): {
            process.Direction.LEFTWARDS,
            process.Direction.RIGHTWARDS,
        },
        process.Coords(3, 7): {
            process.Direction.LEFTWARDS,
            process.Direction.RIGHTWARDS,
        },
        process.Coords(4, 7): {process.Direction.UPWARDS},
        process.Coords(5, 7): {process.Direction.DOWNWARDS},
        process.Coords(6, 7): {process.Direction.DOWNWARDS},
        process.Coords(7, 7): {process.Direction.UPWARDS},
        process.Coords(1, 8): {process.Direction.UPWARDS, process.Direction.DOWNWARDS},
        process.Coords(2, 8): {process.Direction.LEFTWARDS},
        process.Coords(3, 8): {process.Direction.LEFTWARDS},
        process.Coords(4, 8): {process.Direction.LEFTWARDS},
        process.Coords(5, 8): {
            process.Direction.LEFTWARDS,
            process.Direction.DOWNWARDS,
        },
        process.Coords(6, 8): {
            process.Direction.LEFTWARDS,
            process.Direction.RIGHTWARDS,
        },
        process.Coords(7, 8): {process.Direction.UPWARDS, process.Direction.DOWNWARDS},
        process.Coords(1, 9): {process.Direction.DOWNWARDS},
        process.Coords(5, 9): {process.Direction.DOWNWARDS},
        process.Coords(7, 9): {process.Direction.DOWNWARDS},
    }
    assert best_tile_num == 51
