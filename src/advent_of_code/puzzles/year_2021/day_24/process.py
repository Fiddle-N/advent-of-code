"""
2021 Day 24

An ALU (arithmetic logic unit) is a 4D processing unit with four
registers - w, x, y and z, all initialised to 0 - and six instructions:

inp a - read an input and write to a.
add a b - add a to b and write to a.
mul a b - multiply a with b and write to a.
div a b - floor-divide a with b and write to a.
mod a b - get the remainder of a divided with b and write to a.
eql a b - if a equals b, write 1 to a, else write 0 to a.

You are given a program called MONAD that validates a 14 digit number
where each digit is 1-9. MONAD takes in 14 inputs corresponding to the
14 individual digits from left to right, and if the number is valid,
leaves the z register as 0.

Part 1
Find the greatest number accepted by MONAD.

Part 2
Find the smallest number accepted by MONAD.

Solution

MONAD is a program of 14 repeating chunks of instructions that follow the
below pattern:

inp w
mul x 0
add x z
mod x 26
div z {div_z}
add x {add_x}
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y {add_y}
mul y x
add z y

where div_z is seven times as 1 and seven times as 26, add_x is an integer
where seven are greater than 10 and seven are 0 or less, and add_y is always
a positive integer.

z must always equal 0 at the very end.
There are three operations that change z:

div z {div_z}
mul z y
add z y

Let's consider the block of code that ends in "add z y", which is the last
operation of the chunk and therefore the program:

eql x w
eql x 0
...
mul y 0
add y w
add y {add_y}
mul y x
add z y

y is zeroed, and then either added to a w (which never changes), add_y
(which is a positive integer), or multiplied to with x (which is 0 or 1).
This is then added to z. So for z to be 0, since y cannot be positive,
x must be 0 to zero y. Which means that w must be equal to x in the "eql"
block at the very end.

Let's now also consider the "mul z y" block:

eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y

When x is 1, y is 26 and z is multiplied by 26.
When x is 0, y is 1 and z is multiplied by 1.
It stands to reason, then than we want x to be equal to w as many times as
possible to limit the growth of z. z is divided by 26 only seven times, so we
can only let z be multiplied by 26 seven times.

Now, let's consider the code block that determines whether x is equal to w:

mul x 0
add x z
mod x 26
div z {div_z}
add x {add_x}
eql x w
eql x 0

x undergoes the modulo operator to be between 0 and 25. But then it is added to
add_x before undergoing the x == w check. However, in the seven times that add_x
is greater than 10, it is impossible for x to equal w as w is between 1-9 and never
gets changed.

This means, then, that x can only equal w the other seven times. And must equal w
the other seven times, in order to limit the growth of z and have a chance that z
equals 0 by the end.

The solution below recursively splits the program into the fourteen chunks, but it
also splits into the seven sections where x must be 0. At each of these larger sections,
we check to see if x is equal to 0, and then discard multiple overlapping options.
For example, for the same numeric outputs, if z is the same value at the end of a
section, we can keep either the greatest or smallest output (depending on part 1 vs 2)
and discard the rest. This greatly reduces the number of operations to check
overall.
"""

import re
from typing import Literal

from advent_of_code.common import read_file, timed_run
from advent_of_code.puzzles.year_2021.day_24.alu_vm import (
    Registers,
    execute_instructions,
    parse_instructions,
)

MODEL_NO_DIGITS = 14

SINGLE_DIGIT_INSTRUCTIONS_PATTERN = """\
inp w
mul x 0
add x z
mod x 26
div z {div_z}
add x {add_x}
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y {add_y}
mul y x
add z y"""

SINGLE_DIGIT_INSTRUCTIONS_PATTERN_RE = SINGLE_DIGIT_INSTRUCTIONS_PATTERN.format(
    div_z=r"(?P<div_z_operand>-?\d+)",
    add_x=r"(?P<add_x_operand>-?\d+)",
    add_y=r"(?P<add_y_operand>-?\d+)",
)


def parse_variable_operands(instruction_text: str) -> list[dict[str, int]]:
    variable_operands = []
    iter_chunks = re.finditer(SINGLE_DIGIT_INSTRUCTIONS_PATTERN_RE, instruction_text)
    for match_ in iter_chunks:
        variable_operands.append(
            {
                "div_z": int(match_.group("div_z_operand")),
                "add_x": int(match_.group("add_x_operand")),
                "add_y": int(match_.group("add_y_operand")),
            }
        )
    assert len(variable_operands) == MODEL_NO_DIGITS
    return variable_operands


class ModelNumberValidation:
    def __init__(self, instruction_text: str):
        self.single_digit_instructions = parse_instructions(
            SINGLE_DIGIT_INSTRUCTIONS_PATTERN
        )
        self.variable_operands = parse_variable_operands(instruction_text)
        self.section_positions = []
        for pos, var_op in enumerate(self.variable_operands):
            if var_op["add_x"] < 10:
                self.section_positions.append(pos)
        self.largest_model_number_range = range(9, 0, -1)
        self.smallest_model_number_range = range(1, 10)
        self._range: range

    def _validate_digit(
        self, pos: int, digit: int, end_pos: int, registers: Registers
    ) -> list[tuple[str, Registers]]:
        var_ops = self.variable_operands[pos]

        output_registers = execute_instructions(
            self.single_digit_instructions,
            [digit],
            var_ops,
            registers,
        )

        # base case
        if pos == end_pos:
            if output_registers.x == 0:
                return [(str(digit), output_registers)]
            return []

        # recursive case
        results = []
        for next_digit in self._range:
            result = self._validate_digit(
                pos + 1, next_digit, end_pos, output_registers
            )
            if not result:
                continue

            for model_no_suffix, next_registers in result:
                result_suffix = str(digit) + model_no_suffix

                results.append((result_suffix, next_registers))

        return results

    def _validate_section(
        self,
        start_pos: int,
        chunk_pos: int,
        registers: Registers,
    ) -> str | None:
        end_pos = self.section_positions[chunk_pos]
        results = {}
        for digit in self._range:
            result = self._validate_digit(start_pos, digit, end_pos, registers)

            for model_no_suffix, output_registers in result:
                if output_registers.z in results:
                    continue
                results[output_registers.z] = (model_no_suffix, output_registers)

        # base case
        if chunk_pos == len(self.section_positions) - 1:
            for z, (suffix, final_registers) in results.items():
                if z == 0:
                    return suffix
            return None

        # recursive case
        for next_model_no_prefix, next_register in results.values():
            suffix = self._validate_section(
                start_pos=end_pos + 1, chunk_pos=chunk_pos + 1, registers=next_register
            )
            if suffix is not None:
                return next_model_no_prefix + suffix

        return None

    def validate(self, mode: Literal["smallest", "largest"]) -> str:
        self._range = (
            self.largest_model_number_range
            if mode == "largest"
            else self.smallest_model_number_range
        )
        result = self._validate_section(start_pos=0, chunk_pos=0, registers=Registers())
        if result is None:
            raise ValueError("A result was not found")
        return result


def run():
    instruction_text = read_file()
    model_number_validation = ModelNumberValidation(instruction_text)
    print(model_number_validation.validate(mode="largest"))
    print(model_number_validation.validate(mode="smallest"))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
