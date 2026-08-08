import re
from itertools import count
from dataclasses import dataclass
from string import ascii_lowercase

from advent_of_code.common import read_file, timed_run

SPIN_PATTERN = r"s(?P<no_programs>\d+)"
EXCHANGE_PATTERN = r"x(?P<pos_a>\d+)/(?P<pos_b>\d+)"
PARTNER_PATTERN = r"p(?P<prog_a>\w)/(?P<prog_b>\w)"

ONE_BILLION = 1_000_000_000


@dataclass(frozen=True)
class Spin:
    no_programs: int


@dataclass(frozen=True)
class Exchange:
    pos_a: int
    pos_b: int


@dataclass(frozen=True)
class Partner:
    prog_a: str
    prog_b: str


type Move = Spin | Exchange | Partner


def parse(raw_moves: str) -> list[Move]:
    moves = []
    for raw_move in raw_moves.split(","):
        if spin_match := re.fullmatch(SPIN_PATTERN, raw_move):
            move = Spin(no_programs=int(spin_match["no_programs"]))
        elif exchange_match := re.fullmatch(EXCHANGE_PATTERN, raw_move):
            move = Exchange(
                pos_a=int(exchange_match["pos_a"]), pos_b=int(exchange_match["pos_b"])
            )
        elif partner_match := re.fullmatch(PARTNER_PATTERN, raw_move):
            move = Partner(
                prog_a=partner_match["prog_a"], prog_b=partner_match["prog_b"]
            )
        else:
            raise ValueError("no move match")
        moves.append(move)
    return moves


def dance(programs: str, moves: list[Move]) -> tuple[str, list[str]]:
    progs = list(programs)
    dance_cycle = [programs]
    for cycle in count():
        for move in moves:
            match move:
                case Spin(no_programs):
                    progs = progs[-no_programs:] + progs[:-no_programs]
                case Exchange(pos_a, pos_b):
                    progs[pos_a], progs[pos_b] = progs[pos_b], progs[pos_a]
                case Partner(prog_a, prog_b):
                    pos_a = progs.index(prog_a)
                    pos_b = progs.index(prog_b)
                    progs[pos_a], progs[pos_b] = progs[pos_b], progs[pos_a]
        danced_progs = "".join(progs)
        if cycle == 0:
            initial_dance = danced_progs
        if danced_progs in dance_cycle:
            return initial_dance, dance_cycle
        dance_cycle.append(danced_progs)
    raise Exception("unreachable code")


def watch_dance(programs: str, moves: list[Move]) -> tuple[str, str]:
    initial_dance, dance_cycle = dance(programs, moves)
    final_dance = dance_cycle[ONE_BILLION % len(dance_cycle)]
    return initial_dance, final_dance


def run():
    raw_moves = read_file()
    moves = parse(raw_moves)
    progs = ascii_lowercase[:16]
    print(watch_dance(progs, moves))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
