import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import Self

from advent_of_code.common import read_file, timed_run

PROGRAM_PATTERN = r"(?P<name>\w+) \((?P<weight>\d+)\)( -> (?P<subprograms>[\w, ]+))?"


@dataclass
class Program:
    name: str
    weight: int
    subprograms: list["Program"]

    @cached_property
    def total_weight(self: Self) -> int:
        return self.weight + sum(
            subprogram.total_weight for subprogram in self.subprograms
        )


class ProgramParser:
    def __init__(self):
        self._parsed_programs = {}
        self._transformed_programs = {}
        self._last_program = None

    def _parse_syntax(self, raw_programs: str) -> None:
        for raw_program in raw_programs.splitlines():
            match = re.fullmatch(PROGRAM_PATTERN, raw_program)
            assert match
            subprograms = (
                match["subprograms"].split(", ") if match["subprograms"] else []
            )
            self._parsed_programs[match["name"]] = (int(match["weight"]), subprograms)

    def _transform_program(self, name: str) -> Program:
        if name in self._transformed_programs:
            return self._transformed_programs[name]
        weight, subprogram_names = self._parsed_programs[name]
        subprograms = [
            self._transform_program(subprogram_name)
            for subprogram_name in subprogram_names
        ]
        program = Program(name, weight, subprograms)
        self._transformed_programs[name] = program
        self._last_program = program
        return program

    def _transform(self) -> None:
        for program_name in self._parsed_programs:
            self._transform_program(program_name)

    def parse(self, raw_programs: str) -> Program:
        self._parse_syntax(raw_programs)
        self._transform()
        assert self._last_program is not None
        return self._last_program


def _seek_unbalanced_weight(
    program: Program, desirable_weight: int | None = None
) -> int:
    program_weights = defaultdict(list)
    for subprogram in program.subprograms:
        program_weights[subprogram.total_weight].append(subprogram)

    if len(program_weights) == 1:
        # found unbalanced program
        assert desirable_weight is not None
        subprogram_weight = next(iter(program_weights))
        return desirable_weight - (subprogram_weight * len(program.subprograms))

    # recurse
    assert len(program_weights) == 2
    unbalanced = [
        (weight, subprograms[0])
        for weight, subprograms in program_weights.items()
        if len(subprograms) == 1
    ]
    assert len(unbalanced) == 1
    unbalanced_weight, unbalanced_subprogram = unbalanced[0]
    balanced = program_weights.keys() - {unbalanced_weight}
    balanced_weight = next(iter(balanced))
    return _seek_unbalanced_weight(unbalanced_subprogram, balanced_weight)


def seek_unbalanced_weight(program: Program) -> int:
    return _seek_unbalanced_weight(program)


def run():
    raw_programs = read_file()
    pp = ProgramParser()
    program = pp.parse(raw_programs)
    print(program.name)
    print(seek_unbalanced_weight(program))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
