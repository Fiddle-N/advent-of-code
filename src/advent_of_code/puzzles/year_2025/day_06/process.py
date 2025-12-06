from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal
from math import prod
from itertools import groupby

from advent_of_code.common import read_file, timed_run


Operator = Literal["+", "*"]


OPERATOR_FNS: dict[Operator, Callable[[list[int]], int]] = {"+": sum, "*": prod}


@dataclass(frozen=True)
class MathExpr:
    operands: list[int]
    operator: Operator


def parse(raw_input: str, mode: Literal["part_1", "part_2"]) -> list[MathExpr]:
    lines = raw_input.rstrip().splitlines()
    raw_operands = lines[:-1]
    raw_operators = lines[-1]

    if mode == "part_2":
        transposed_lines = list(zip(*raw_operands))
        grouped_lines = groupby(
            transposed_lines, key=lambda seq: all(val == " " for val in seq)
        )
        transposed_operands = [
            [int("".join(num)) for num in group]
            for key, group in grouped_lines
            if not key
        ]
    else:
        untransposed_operands = [
            [int(operand) for operand in operands.split()] for operands in raw_operands
        ]
        transposed_operands = list(zip(*untransposed_operands))
    untransposed_operators = raw_operators.split()
    transposed = zip(transposed_operands, untransposed_operators)
    math_exprs = [
        MathExpr(list(operands), operator) for operands, operator in transposed
    ]
    return math_exprs


def calculate(exprs: list[MathExpr]) -> int:
    return sum(OPERATOR_FNS[expr.operator](expr.operands) for expr in exprs)


def run():
    raw_math = read_file()
    exprs_1 = parse(raw_math, "part_1")
    print(calculate(exprs_1))
    exprs_2 = parse(raw_math, "part_2")
    print(calculate(exprs_2))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
