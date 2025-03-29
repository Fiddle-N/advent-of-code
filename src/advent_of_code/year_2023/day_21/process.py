import dataclasses
import enum
from typing import Self


STARTING_POSITION = "S"

ORIGINAL_ELF_STEP_GOAL = 64
NEW_ELF_STEP_GOAL = 26501365

GARDEN_LENGTH = 131
START_TO_GARDEN_EDGE_LENGTH = 65


class GardenSpace(enum.Enum):
    PLOT = "."
    ROCK = "#"


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Coords(self.x + other.x, self.y + other.y)


@dataclasses.dataclass
class ElfStepResult:
    new_plots: set[Coords]
    plots_reached: int
    all_plots: set[Coords] | None = None


OFFSET_COORDS = [
    Coords(0, -1),
    Coords(0, 1),
    Coords(-1, 0),
    Coords(1, 0),
]


class Garden:
    def __init__(self, garden_input):
        garden_rows = garden_input.splitlines()

        self.width = len(garden_rows[0])
        self.height = len(garden_rows)
        self.max_x = self.width - 1
        self.max_y = self.height - 1

        self.garden = {}
        for y, row in enumerate(garden_input.splitlines()):
            for x, space_str in enumerate(row):
                coords = Coords(x, y)
                if space_str == STARTING_POSITION:
                    space = GardenSpace.PLOT
                    self.start = coords
                else:
                    space = GardenSpace(space_str)
                self.garden[coords] = space

        self.garden_plots = {
            coords for coords, space in self.garden.items() if space == GardenSpace.PLOT
        }

    @classmethod
    def read_file(cls) -> Self:
        with open("input.txt") as f:
            return cls(f.read())


def normalise_pos(garden, pos):
    norm_x = pos.x % garden.width
    norm_y = pos.y % garden.height
    return Coords(norm_x, norm_y)


class ElfStepCalculator:
    def __init__(self, garden: Garden, is_infinite=False, include_full_plot_info=False):
        self.garden = garden
        self.is_infinite = is_infinite
        self.include_full_plot_info = include_full_plot_info

    def _new_positions(self, positions):
        next_positions = set()
        for pos in positions:
            new_positions = [(pos + offset) for offset in OFFSET_COORDS]
            valid_new_positions = []
            for new_pos in new_positions:
                normalised_pos = new_pos
                if self.is_infinite:
                    normalised_pos = normalise_pos(self.garden, new_pos)
                if normalised_pos in self.garden.garden_plots:
                    valid_new_positions.append(new_pos)
            next_positions.update(valid_new_positions)
        return next_positions

    def __iter__(self):
        penult_output = None
        last_output = ElfStepResult(
            new_plots={self.garden.start},
            all_plots={self.garden.start} if self.include_full_plot_info else None,
            plots_reached=1,
        )

        while True:
            positions = self._new_positions(last_output.new_plots)
            if penult_output is None:
                output = ElfStepResult(
                    new_plots=positions,
                    all_plots=positions if self.include_full_plot_info else None,
                    plots_reached=len(positions),
                )
            else:
                new_positions = positions - penult_output.new_plots
                output = ElfStepResult(
                    new_plots=new_positions,
                    all_plots=(positions | penult_output.all_plots)
                    if self.include_full_plot_info
                    else None,
                    plots_reached=penult_output.plots_reached + len(new_positions),
                )

            yield output

            penult_output = last_output
            last_output = output


def total_corner_plots(visited_plot_locations):
    # Produce the number of visited plots
    # for each half-distance corner of the original plot
    # These are the regions that would be explored on a 7 x 7 plot
    # AAA.BBB
    # AA...BB
    # A.....B
    # .......
    # C.....D
    # CC...DD
    # CCC.DDD
    # The real plot is 131 x 131 with the corners scaled up to length 65
    #
    half_distance = GARDEN_LENGTH // 2

    first_half_start = 0
    first_half_end = first_half_start + half_distance

    last_half_end = GARDEN_LENGTH
    last_half_start = GARDEN_LENGTH - half_distance

    top_left = sum(
        Coords(x, y) in visited_plot_locations
        for y in range(first_half_start, first_half_end)
        for x in range(first_half_start, first_half_end - y)
    )
    top_right = sum(
        Coords(x, y) in visited_plot_locations
        for y in range(first_half_start, first_half_end)
        for x in range(last_half_start + y, last_half_end)
    )
    bottom_left = sum(
        Coords(x, y) in visited_plot_locations
        for count, y in enumerate(range(last_half_start, last_half_end), start=1)
        for x in range(first_half_start, first_half_start + count)
    )
    bottom_right = sum(
        Coords(x, y) in visited_plot_locations
        for count, y in enumerate(range(last_half_start, last_half_end), start=1)
        for x in range(last_half_end - count, last_half_end)
    )

    corner_plots = sum([top_left, top_right, bottom_left, bottom_right])

    return corner_plots


def equation(
    odd_full_garden_plots,
    even_full_garden_plots,
    odd_corner_plots,
    even_corner_plots,
    n,
):
    return (
        (n**2) * odd_full_garden_plots
        + ((n - 1) ** 2) * even_full_garden_plots
        - n * odd_corner_plots
        + (n - 1) * even_corner_plots
    )


def iteration_vs_equation_solution_test(
    garden,
    odd_full_garden_plots,
    even_full_garden_plots,
    odd_corner_plots,
    even_corner_plots,
):
    # n = 1 test
    elf_step_calculator = ElfStepCalculator(garden, is_infinite=True)
    elf_step_iter = iter(elf_step_calculator)
    for _ in range(65):
        result = next(elf_step_iter)
    n_1_iter_result = result.plots_reached

    n_1_eq_result = equation(
        odd_full_garden_plots,
        even_full_garden_plots,
        odd_corner_plots,
        even_corner_plots,
        1,
    )

    assert n_1_iter_result == n_1_eq_result

    # n = 2 test
    for _ in range(131):
        result = next(elf_step_iter)
    n_2_iter_result = result.plots_reached

    n_2_eq_result = equation(
        odd_full_garden_plots,
        even_full_garden_plots,
        odd_corner_plots,
        even_corner_plots,
        2,
    )

    assert n_2_iter_result == n_2_eq_result


def garden_plots_reachable_with_original_step_goal(garden):
    elf_step_calculator = ElfStepCalculator(garden, is_infinite=False)
    elf_step_iter = iter(elf_step_calculator)

    for _ in range(ORIGINAL_ELF_STEP_GOAL):
        result = next(elf_step_iter)

    return result.plots_reached


def garden_plots_reachable_with_new_step_goal(garden, test_equation_solution=False):
    # The step goal is 26501365
    #
    # This is exactly (202300 * 131) + 65
    # where 131 is the distance to traverse a full garden edge-to-edge
    # and 65 the distance to traverse from start to the edge of a garden.
    #
    # This means that we can model plots reached as an equation
    # where n is the number of gardens from the start point to the farthest edge.
    #
    # The plots reached form a diamond structure.
    # So the equation involves multiples of plots that can be reached in one garden
    # and adding/subtracting corners that make up the diamond.
    #
    # Finally, the plots have parity - each garden switches parity as n increases,
    # so a full garden switches between 2 values in terms of how many garden plots are reachable.
    # The corners to be added/removed also have parity.
    #
    # Below are explanatory diagrams:
    # A width of 7 is used, but in reality the garden width is 131.
    #
    # Firstly, the difference between odd parity and even parity
    # where plots reached are denoted with O and S is the start spot
    #
    # Odd parity
    #
    # .O.O.O.
    # O.O.O.O
    # .O.O.O.
    # O.OSO.O
    # .O.O.O.
    # O.O.O.O
    # .O.O.O.
    #
    # Even parity (S is a spot that can be reached so is overwritten with O)
    #
    # O.O.O.O
    # .O.O.O.
    # O.O.O.O
    # .O.O.O.
    # O.O.O.O
    # .O.O.O.
    # O.O.O.O
    #
    #
    # Secondly, the gardens involved for increasing numbers of n
    # Odd/even parity is denoted with an O/E in the middle of the garden
    # . represents the diamond area containing the plots we want to know within full gardens
    # A B C D represents four corners of odd parity
    # whose plots need to be subtracted from the value of plots calculated from full gardens
    # a b c d represents four corners of even parity
    # whose plots need to be added to the value of plots calculated from full gardens
    #
    # n = 1
    #
    # AAA.BBB
    # AA...BB
    # A.....B
    # ...O...
    # C.....D
    # CC...DD
    # CCC.DDD
    #
    #
    # n = 2
    #
    #         AAA.BBB
    #         AA...BB
    #         A.....B
    #         ...O...
    #       d ....... c
    #      dd ....... cc
    #     ddd ....... ccc
    #
    # AAA.... ....... ....BBB
    # AA..... ....... .....BB
    # A...... ....... ......B
    # ...O... ...E... ...O...
    # C...... ....... ......D
    # CC..... ....... .....DD
    # CCC.... ....... ....DDD
    #
    #     bbb ....... aaa
    #      bb ....... aa
    #       b ....... a
    #         ...O...
    #         C.....D
    #         CC...DD
    #         CCC.DDD
    #
    #
    # n = 3
    #
    #                 AAA.BBB
    #                 AA...BB
    #                 A.....B
    #                 ...O...
    #               d ....... c
    #              dd ....... cc
    #             ddd ....... ccc
    #
    #         AAA.... ....... ....BBB
    #         AA..... ....... .....BB
    #         A...... ....... ......B
    #         ...O... ...E... ...O...
    #       d ....... ....... ....... c
    #      dd ....... ....... ....... cc
    #     ddd ....... ....... ....... ccc
    #
    # AAA.... ....... ....... ....... ....BBB
    # AA..... ....... ....... ....... .....BB
    # A...... ....... ....... ....... ......B
    # ...O... ...E... ...O... ...E... ...O...
    # C...... ....... ....... ....... ......D
    # CC..... ....... ....... ....... .....DD
    # CCC.... ....... ....... ....... ....DDD
    #
    #     bbb ....... ....... ....... aaa
    #      bb ....... ....... ....... aa
    #       b ....... ....... ....... a
    #         ...O... ...E... ...O...
    #         C...... ....... ......D
    #         CC..... ....... .....DD
    #         CCC.... ....... ....DDD
    #
    #             bbb ....... aaa
    #              bb ....... aa
    #               b ....... a
    #                 ...O...
    #                 C.....D
    #                 CC...DD
    #                 CCC.DDD
    #
    #
    # The above diagrams match the quadratic equation for finding garden plots:
    # n^2 O + (n-1)^2 E - n(A + B + C + D) + (n-1)(a + b + c + d)
    #
    # ---
    # Set test_equation_solution to True to assert equation solution against iteration solution for correctness
    # Set test_equation_solution to False for performance
    #
    elf_step_calculator = ElfStepCalculator(
        garden, is_infinite=False, include_full_plot_info=True
    )
    elf_step_iter = iter(elf_step_calculator)

    for _ in range(GARDEN_LENGTH - 2):
        odd_full_garden_result = next(elf_step_iter)

    even_full_garden_result = next(elf_step_iter)

    odd_full_garden_plots = odd_full_garden_result.plots_reached
    even_full_garden_plots = even_full_garden_result.plots_reached

    odd_plot_locations = odd_full_garden_result.all_plots
    even_plot_locations = even_full_garden_result.all_plots

    odd_corner_plots = total_corner_plots(odd_plot_locations)
    even_corner_plots = total_corner_plots(even_plot_locations)

    if test_equation_solution:
        iteration_vs_equation_solution_test(
            garden,
            odd_full_garden_plots,
            even_full_garden_plots,
            odd_corner_plots,
            even_corner_plots,
        )

    n = (NEW_ELF_STEP_GOAL - START_TO_GARDEN_EDGE_LENGTH) // GARDEN_LENGTH + 1
    result = equation(
        odd_full_garden_plots,
        even_full_garden_plots,
        odd_corner_plots,
        even_corner_plots,
        n,
    )
    return result


def main():
    garden = Garden.read_file()
    print(
        f"Garden plots that the elf can reach in {ORIGINAL_ELF_STEP_GOAL} steps:",
        garden_plots_reachable_with_original_step_goal(garden),
    )
    print(
        f"Garden plots that the elf can reach in {NEW_ELF_STEP_GOAL} steps:",
        garden_plots_reachable_with_new_step_goal(garden, test_equation_solution=False),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
