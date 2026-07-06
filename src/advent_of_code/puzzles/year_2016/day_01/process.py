import dataclasses
from typing import Literal

from advent_of_code.common import (
    read_file,
    timed_run,
    Coords,
    CardinalDirections,
    Turn,
    turn_cardinal_direction,
    FOUR_POINT_CARDINAL_DIRECTION_TO_COORDS,
)

STARTING_DIR = CardinalDirections.NORTH


@dataclasses.dataclass(frozen=True)
class Instr:
    turn: Turn
    val: int


def parse_instrs(raw_instrs: str) -> list[Instr]:
    instrs = []
    for raw_instr in raw_instrs.split(", "):
        turn, val = raw_instr[:1], raw_instr[1:]
        instrs.append(Instr(Turn(turn), int(val)))
    return instrs


def _run_instrs_to_end(pos: Coords, instrs: list[Instr]) -> Coords:
    dir_ = STARTING_DIR

    for instr in instrs:
        dir_ = turn_cardinal_direction(dir_, turn=instr.turn, no_of_turns=1)
        trans_pos = FOUR_POINT_CARDINAL_DIRECTION_TO_COORDS[dir_]
        pos = Coords(
            pos.x + (trans_pos.x * instr.val), pos.y + (trans_pos.y * instr.val)
        )

    return pos


def _run_instrs_to_ebhq(pos: Coords, instrs: list[Instr]) -> Coords:
    # ebhq is the first location you visit twice
    dir_ = STARTING_DIR
    seen = set()

    for instr in instrs:
        dir_ = turn_cardinal_direction(dir_, turn=instr.turn, no_of_turns=1)
        trans_pos = FOUR_POINT_CARDINAL_DIRECTION_TO_COORDS[dir_]

        for _ in range(instr.val):
            seen.add(pos)
            pos = Coords(pos.x + trans_pos.x, pos.y + trans_pos.y)
            if pos in seen:
                return pos

    raise ValueError


def run_instrs(instrs: list[Instr], dest: Literal["end", "ebhq"]):
    start = Coords(0, 0)
    end = (
        _run_instrs_to_end(start, instrs)
        if dest == "end"
        else _run_instrs_to_ebhq(start, instrs)
    )
    return start.manhatten_distance(end)


def run():
    raw_instrs = read_file()
    instrs = parse_instrs(raw_instrs)
    print(run_instrs(instrs, dest="end"))
    print(run_instrs(instrs, dest="ebhq"))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
