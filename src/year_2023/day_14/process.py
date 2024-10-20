import enum
import itertools

ROUNDED_ROCKS = 'O'
CUBE_ROCKS = '#'
EMPTY_SPACE = '.'


class Direction(enum.Enum):
    NORTH = enum.auto()
    WEST = enum.auto()
    SOUTH = enum.auto()
    EAST = enum.auto()


VERTICAL_TILTS = [Direction.NORTH, Direction.SOUTH]
LEFT_TILTS = [Direction.NORTH, Direction.WEST]
CYCLE_DIRECTIONS = [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]


def _tilt_section(section, direction):
    length = len(section)
    rock_no = len([space for space in section if space == ROUNDED_ROCKS])
    empty_space_no = length - rock_no
    rocks = [ROUNDED_ROCKS] * rock_no
    empty_spaces = [EMPTY_SPACE] * empty_space_no
    tilted_spaces = (
        rocks + empty_spaces
        if direction in LEFT_TILTS
        else empty_spaces + rocks
    )
    tilted_section = ''.join(tilted_spaces)
    return tilted_section


def tilt(platform, direction=Direction.NORTH):
    platform_lines = platform.splitlines()
    if direction in VERTICAL_TILTS:
        platform_lines = list(''.join(col) for col in zip(*platform_lines))
    tilted_lines = []
    for line in platform_lines:
        sections = line.split(CUBE_ROCKS)
        tilted_sections = [_tilt_section(section, direction) for section in sections]
        tilted_line = CUBE_ROCKS.join(tilted_sections)
        tilted_lines.append(tilted_line)
    if direction in VERTICAL_TILTS:
        tilted_lines = list(''.join(col) for col in zip(*tilted_lines))
    tilted_platform = '\n'.join(tilted_lines)
    return tilted_platform


def cycle(platform, total_cycles=1):
    platforms = [platform]
    for cycle_no in itertools.count():
        for direction in CYCLE_DIRECTIONS:
            platform = tilt(platform, direction)
        if cycle_no == total_cycles:
            return platform
        if platform in platforms:
            offset = platforms.index(platform)
            cycle_length = len(platforms) - offset
            result_platform = platforms[(total_cycles - offset) % cycle_length + offset]
            return result_platform
        platforms.append(platform)
        yield platform


def calculate_load(platform):
    platform_rows = platform.splitlines()
    load = 0
    for row_no, row in enumerate(platform_rows):
        load_per_rock = len(platform_rows) - row_no
        rock_no = len([space for space in row if space == ROUNDED_ROCKS])
        load += (load_per_rock * rock_no)
    return load


def read_file():
    with open("input.txt") as f:
        return f.read()


def main() -> None:
    platform_input = read_file()

    tilted_platform = tilt(platform_input)
    load = calculate_load(tilted_platform)
    print(
        "Total load on north support beams:",
        load
    )

    many_cycles_no = 1_000_000_000
    cycle_iter = cycle(platform_input, total_cycles=1_000_000_000)
    while True:
        try:
            next(cycle_iter)
        except StopIteration as exc:
            titled_platform_after_many_cycles = exc.value
            break
    load_after_many_cycles = calculate_load(titled_platform_after_many_cycles)
    print(
        f"Total load on north support beams after {many_cycles_no}:",
        load_after_many_cycles
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
