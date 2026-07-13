from typing import Literal

from advent_of_code.common import (
    read_file,
    timed_run,
    Coords,
    Direction,
    DIRECTION_LETTERS_TO_DIRECTION,
    FOUR_POINT_DIRECTION_TO_COORDS,
)

IMAGINARY_KEYPAD = {
    Coords(-1, -1): "1",
    Coords(0, -1): "2",
    Coords(1, -1): "3",
    Coords(-1, 0): "4",
    Coords(0, 0): "5",
    Coords(1, 0): "6",
    Coords(-1, 1): "7",
    Coords(0, 1): "8",
    Coords(1, 1): "9",
}

KEYPAD = {
    Coords(2, -2): "1",
    Coords(1, -1): "2",
    Coords(2, -1): "3",
    Coords(3, -1): "4",
    Coords(0, 0): "5",
    Coords(1, 0): "6",
    Coords(2, 0): "7",
    Coords(3, 0): "8",
    Coords(4, 0): "9",
    Coords(1, 1): "A",
    Coords(2, 1): "B",
    Coords(3, 1): "C",
    Coords(2, 2): "D",
}


def parse_instrs(raw_input: str) -> list[list[Direction]]:
    return [
        [DIRECTION_LETTERS_TO_DIRECTION[letter] for letter in line]
        for line in raw_input.splitlines()
    ]


def calculate_code(
    instrs: list[list[Direction]], keypad_type: Literal["imaginary", "real"]
) -> str:
    keypad = IMAGINARY_KEYPAD if keypad_type == "imaginary" else KEYPAD
    code = ""
    pos = Coords(0, 0)
    for instr in instrs:
        for dir_ in instr:
            trans_coords = FOUR_POINT_DIRECTION_TO_COORDS[dir_]
            new_pos = pos + trans_coords
            if new_pos in keypad:
                pos = new_pos
        code += keypad[pos]
    return code


def run():
    raw_instrs = read_file()
    instrs = parse_instrs(raw_instrs)
    print(calculate_code(instrs, keypad_type="imaginary"))
    print(calculate_code(instrs, keypad_type="real"))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
