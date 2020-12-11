from day11 import process


class TestTheoreticalModel:

    def test_theoretical_single_model_runs(self):
        grid_0 = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

        grid_1 = """\
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##"""

        grid_2 = """\
#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##"""

        grid_3 = """\
#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##"""

        grid_4 = """\
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##"""

        grid_5 = """\
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##"""

        grid_6 = grid_5

        seating_system = process.SeatingSystem(grid_0)
        model = process.TheoreticalSeatingSystemModel(seating_system)
        assert seating_system.output_grid(next(model)) == grid_1
        assert seating_system.output_grid(next(model)) == grid_2
        assert seating_system.output_grid(next(model)) == grid_3
        assert seating_system.output_grid(next(model)) == grid_4
        assert seating_system.output_grid(next(model)) == grid_5
        assert seating_system.output_grid(next(model)) == grid_6


    def test_theoretical_full_model_run(self):
        grid = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

        assert process.run_model(process.TheoreticalSeatingSystemModel, grid) == 37


class TestRealModel:

    def test_real_model_adjacent_seats_1(self):
        grid = """\
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#....."""

        # arrange
        seating_system = process.SeatingSystem(grid)
        empty_seat, = [seat_coords for seat_coords, seat in seating_system.seats.items() if seat == process.EMPTY]
        occupied_seats = {seat_coords for seat_coords, seat in seating_system.seats.items() if seat == process.OCCUPIED}

        # act
        model = process.RealSeatingSystemModel(seating_system)

        # assert
        assert set(model.adj_seats[empty_seat]) == occupied_seats


    def test_real_model_adjacent_seats_2(self):
        grid = """\
.............
.L.L.#.#.#.#.
............."""

        # arrange
        seating_system = process.SeatingSystem(grid)
        empty_seats = [seat_coords for seat_coords, seat in seating_system.seats.items() if seat == process.EMPTY]

        # act
        model = process.RealSeatingSystemModel(seating_system)

        # assert
        expected_empty_seat, = model.adj_seats[empty_seats[0]]
        actual_empty_seat = empty_seats[1]
        assert expected_empty_seat == actual_empty_seat  # assert left empty seat can only see right empty seat


    def test_real_model_adjacent_seats_3(self):
        grid = """\
.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##."""

        # arrange
        seating_system = process.SeatingSystem(grid)
        empty_seat, = [seat_coords for seat_coords, seat in seating_system.seats.items() if seat == process.EMPTY]

        # act
        model = process.RealSeatingSystemModel(seating_system)

        # assert
        assert not len(model.adj_seats[empty_seat])

    def test_real_single_model_runs(self):
        grid_0 = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

        grid_1 = """\
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##"""

        grid_2 = """\
#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#"""

        grid_3 = """\
#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#"""

        grid_4 = """\
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#"""

        grid_5 = """\
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#"""

        grid_6 = """\
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#"""

        grid_7 = grid_6

        seating_system = process.SeatingSystem(grid_0)
        model = process.RealSeatingSystemModel(seating_system)
        assert seating_system.output_grid(next(model)) == grid_1
        assert seating_system.output_grid(next(model)) == grid_2
        assert seating_system.output_grid(next(model)) == grid_3
        assert seating_system.output_grid(next(model)) == grid_4
        assert seating_system.output_grid(next(model)) == grid_5
        assert seating_system.output_grid(next(model)) == grid_6
        assert seating_system.output_grid(next(model)) == grid_7

    def test_real_full_model_run(self):
        grid_0 = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

        assert process.run_model(process.RealSeatingSystemModel, grid_0) == 26
