import re
from collections import deque
from dataclasses import dataclass

from advent_of_code.common import read_file, timed_run

PASSWORD = "abcdefgh"
SCRAMBLED_PASSWORD = "fbgdceah"


@dataclass(frozen=True)
class SwapPositions:
    idx_x: int
    idx_y: int


@dataclass(frozen=True)
class SwapLetters:
    char_x: str
    char_y: str


@dataclass(frozen=True)
class RotateSteps:
    steps: int


@dataclass(frozen=True)
class RotateLetterBased:
    char: str


@dataclass(frozen=True)
class ReversePositions:
    start: int
    end: int


@dataclass(frozen=True)
class Move:
    source: int
    target: int


type Instruction = (
    SwapPositions
    | SwapLetters
    | RotateSteps
    | RotateLetterBased
    | ReversePositions
    | Move
)


def parse_instrs(raw_instrs: str) -> list[Instruction]:
    instrs = []
    for raw_instr in raw_instrs.splitlines():
        if match_ := re.fullmatch(
            r"swap position (?P<idx_x>\d+) with position (?P<idx_y>\d+)", raw_instr
        ):
            instr = SwapPositions(int(match_["idx_x"]), int(match_["idx_y"]))
        elif match_ := re.fullmatch(
            r"swap letter (?P<char_x>\w) with letter (?P<char_y>\w)", raw_instr
        ):
            instr = SwapLetters(match_["char_x"], match_["char_y"])
        elif match_ := re.fullmatch(
            r"rotate (?P<dir>left|right) (?P<pos>\d+) steps?", raw_instr
        ):
            sign = -1 if match_["dir"] == "left" else 1
            instr = RotateSteps(int(match_["pos"]) * sign)
        elif match_ := re.fullmatch(
            r"rotate based on position of letter (?P<char>\w)", raw_instr
        ):
            instr = RotateLetterBased(match_["char"])
        elif match_ := re.fullmatch(
            r"reverse positions (?P<start>\d+) through (?P<end>\d+)", raw_instr
        ):
            instr = ReversePositions(int(match_["start"]), int(match_["end"]))
        elif match_ := re.fullmatch(
            r"move position (?P<source>\d+) to position (?P<target>\d+)", raw_instr
        ):
            instr = Move(int(match_["source"]), int(match_["target"]))
        else:
            raise ValueError("Instruction does not match existing pattern")
        instrs.append(instr)
    return instrs


def swap_positions(pw: list[str], idx_x: int, idx_y: int) -> None:
    (pw[idx_x], pw[idx_y]) = (pw[idx_y], pw[idx_x])


def swap_letters(pw: list[str], char_x: str, char_y: str) -> None:
    idx_x = pw.index(char_x)
    idx_y = pw.index(char_y)
    swap_positions(pw, idx_x, idx_y)


def rotate_steps(pw: list[str], steps: int) -> list[str]:
    deq = deque(pw)
    deq.rotate(steps)
    return list(deq)


def reverse_positions(pw: list[str], start: int, end: int) -> list[str]:
    return pw[:start] + list(reversed(pw[start : end + 1])) + pw[end + 1 :]


def move(pw: list[str], source: int, target: int) -> None:
    char = pw.pop(source)
    pw.insert(target, char)


def scramble(password: str, instrs: list[Instruction]) -> str:
    pw = list(password)
    for instr in instrs:
        match instr:
            case SwapPositions(idx_x, idx_y):
                swap_positions(pw, idx_x, idx_y)
            case SwapLetters(char_x, char_y):
                swap_letters(pw, char_x, char_y)
            case RotateSteps(steps):
                pw = rotate_steps(pw, steps)
            case RotateLetterBased(char):
                idx = pw.index(char)
                deq = deque(pw)
                deq.rotate(1)
                deq.rotate(idx)
                if idx >= 4:
                    deq.rotate(1)
                pw = list(deq)
            case ReversePositions(start, end):
                pw = reverse_positions(pw, start, end)
            case Move(source, target):
                move(pw, source, target)
    return "".join(pw)


def unscramble(password: str, instrs: list[Instruction]) -> str:
    pw = list(password)
    for instr in reversed(instrs):
        match instr:
            case SwapPositions(idx_x, idx_y):
                swap_positions(pw, idx_x, idx_y)
            case SwapLetters(char_x, char_y):
                swap_letters(pw, char_x, char_y)
            case RotateSteps(steps):
                pw = rotate_steps(pw, -steps)
            case RotateLetterBased(char):
                deq = deque(pw)
                rotates = 0
                while True:
                    deq.rotate(-1)
                    rotates += 1
                    if rotates == 5:
                        # impossible number of rotates
                        continue
                    expected_idx = rotates - 1 - (1 if rotates >= 6 else 0)
                    if deq[expected_idx] == char:
                        break
                pw = list(deq)
            case ReversePositions(start, end):
                pw = reverse_positions(pw, start, end)
            case Move(source, target):
                move(pw, target, source)
    return "".join(pw)


def run():
    raw_instrs = read_file()
    instrs = parse_instrs(raw_instrs)
    my_scrambled_password = scramble(PASSWORD, instrs)
    print(my_scrambled_password)
    assert unscramble(my_scrambled_password, instrs) == PASSWORD
    print(unscramble(SCRAMBLED_PASSWORD, instrs))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
