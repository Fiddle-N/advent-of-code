"""
2017 Day 23

https://adventofcode.com/2017/day/23

When the code is analysed, it is evident that the script is attempting to count the
non-primes in a sequence of numbers, by calculating:
2 * 2 == num, 2 * 3 == num, 2 * 4 == num, ..., 2 * factor_b == num
3 * 2 == num, 3 * 3 == num, 3 * 4 == num, ..., 3 * factor_b == num
...
factor_a * factor_b == num
where neither factor_a nor factor_b exceeds num.

Rewritten in Python, the script resembles the following:

count = 0
for num in range(start, stop + 1, step):
    is_prime = True
    factor_a = 2
    while True:
        factor_b = 2
        while True:
            if factor_a * factor_b == num:
                is_prime = False
            factor_b += 1
            if factor_b == num:
                break
        factor_a += 1
        if factor_a == num:
            break
    if not is_prime:
        count += 1

Replace by calculating all primes up until the final number in the sequence using
the Sieve of Eratosthenes, which is then used to count which numbers in the sequence
are not prime.
"""

import operator
from enum import StrEnum, auto
from dataclasses import dataclass
from itertools import count

from advent_of_code.common import read_file, timed_run


class InstrType(StrEnum):
    SET = auto()
    SUB = auto()
    MUL = auto()
    JNZ = auto()


OPERATIONS = {
    InstrType.SET: lambda a, b: b,
    InstrType.SUB: operator.sub,
    InstrType.MUL: operator.mul,
}


class Reg(str):
    pass


class Val(int):
    pass


@dataclass
class Instr:
    type: InstrType
    args: list[Reg | Val]


def parse(raw_instrs: str) -> list[Instr]:
    instrs = []
    for raw_instr in raw_instrs.splitlines():
        raw_type, *raw_args = raw_instr.split()
        args = []
        for raw_arg in raw_args:
            try:
                arg = Val(raw_arg)
            except ValueError:
                arg = Reg(raw_arg)
            args.append(arg)
        instrs.append(Instr(type=InstrType(raw_type), args=args))
    return instrs


def execute(
    regs: dict[Reg, int],
    instrs: list[Instr],
) -> int:
    idx = 0
    mul_invokes = 0
    while True:
        if idx < 0 or idx >= len(instrs):
            return mul_invokes
        instr = instrs[idx]
        match instr:
            case Instr(
                (InstrType.SET | InstrType.SUB | InstrType.MUL) as instr_type,
                (Reg() as reg, operand),
            ):
                if instr_type == InstrType.MUL:
                    mul_invokes += 1
                operand_val = (
                    regs.get(operand, 0) if isinstance(operand, Reg) else operand
                )
                regs[reg] = OPERATIONS[instr_type](regs.get(reg, 0), operand_val)
                idx += 1
            case Instr(InstrType.JNZ, (condition, offset)):
                condition_val = (
                    regs.get(condition, 0) if isinstance(condition, Reg) else condition
                )
                offset_val = regs.get(offset, 0) if isinstance(offset, Reg) else offset
                if condition_val != 0:
                    idx += offset_val
                else:
                    idx += 1


def _extract(instrs: list[Instr]) -> tuple[int, int, int]:
    match instrs[0]:
        case Instr(InstrType.SET, (Reg("b"), Val(b_init))):
            pass
        case _:
            raise ValueError
    match instrs[4]:
        case Instr(InstrType.MUL, (Reg("b"), Val(b_mul))):
            pass
        case _:
            raise ValueError
    match instrs[5]:
        case Instr(InstrType.SUB, (Reg("b"), Val(b_offset))):
            pass
        case _:
            raise ValueError
    match instrs[7]:
        case Instr(InstrType.SUB, (Reg("c"), Val(c_offset))):
            pass
        case _:
            raise ValueError
    match instrs[30]:
        case Instr(InstrType.SUB, (Reg("b"), Val(b_step))):
            pass
        case _:
            raise ValueError

    start = b_init * b_mul - b_offset
    stop = start - c_offset
    step = -b_step

    return start, stop, step


def _sieve_of_eratosthenes(n: int) -> list[bool]:
    # correct between 2 and n
    primes = [True] * (n + 1)
    for num in range(2, int(n**0.5) + 1):
        if primes[num]:
            for incr in count():
                num_multiple = num**2 + incr * num
                if num_multiple > n:
                    break
                primes[num_multiple] = False
    return primes


def optimised_execute(instrs: list[Instr]) -> int:
    start, stop, step = _extract(instrs)
    primes = _sieve_of_eratosthenes(stop)
    return sum(not (primes[num]) for num in range(start, stop + 1, step))


def run():
    raw_instrs = read_file()
    instrs = parse(raw_instrs)
    print(execute(regs={}, instrs=instrs))
    print(optimised_execute(instrs))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
