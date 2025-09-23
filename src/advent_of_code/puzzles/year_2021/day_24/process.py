import dataclasses
import enum
import itertools
import operator
import re
from typing import Literal

from advent_of_code.common import read_file, timed_run

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


class RegisterAttr(enum.StrEnum):
    W = enum.auto()
    X = enum.auto()
    Y = enum.auto()
    Z = enum.auto()


class VariableOperand(enum.StrEnum):
    DIV_Z = enum.auto()
    ADD_X = enum.auto()
    ADD_Y = enum.auto()


class Operator(enum.StrEnum):
    INP = enum.auto()
    ADD = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()
    MOD = enum.auto()
    EQL = enum.auto()


def eql_fn(a, b):
    return 1 if a == b else 0


OPERATOR_FNS = {
    Operator.ADD: operator.add,
    Operator.MUL: operator.mul,
    Operator.DIV: operator.floordiv,
    Operator.MOD: operator.mod,
    Operator.EQL: eql_fn,
}


@dataclasses.dataclass(frozen=True)
class Instruction:
    operator: Operator
    operand_1: RegisterAttr
    operand_2: RegisterAttr | int | VariableOperand | None


@dataclasses.dataclass(frozen=True)
class FrozenRegisters:
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0


@dataclasses.dataclass
class Registers:
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0


def freeze_registers(r: Registers) -> FrozenRegisters:
    return FrozenRegisters(w=r.w, x=r.x, y=r.y, z=r.z)


def unfreeze_registers(fr: FrozenRegisters) -> Registers:
    return Registers(w=fr.w, x=fr.x, y=fr.y, z=fr.z)


@dataclasses.dataclass(frozen=True)
class VariableOperands:
    div_z: int
    add_x: int
    add_y: int


def parse_single_digit_instructions() -> list[Instruction]:
    instructions = []
    for raw_instruction in SINGLE_DIGIT_INSTRUCTIONS_PATTERN.splitlines():
        match raw_instruction.split():
            case [operator_, register_attr]:
                instructions.append(
                    Instruction(
                        Operator(operator_),
                        RegisterAttr(register_attr),
                        None,
                    )
                )
            case [operator_, operand_1, operand_2] if operand_2.startswith(
                "{"
            ) and operand_2.endswith("}"):
                var_operand = operand_2[1:-1]
                instructions.append(
                    Instruction(
                        Operator(operator_),
                        RegisterAttr(operand_1),
                        VariableOperand(var_operand),
                    )
                )
            case [operator_, operand_1, operand_2_str]:
                try:
                    operand_2 = int(operand_2_str)
                except ValueError:
                    operand_2 = RegisterAttr(operand_2_str)
                instructions.append(
                    Instruction(
                        Operator(operator_),
                        RegisterAttr(operand_1),
                        operand_2,
                    )
                )
    return instructions


def parse_variable_operands(instruction_text: str) -> list[VariableOperands]:
    variable_operands = []
    iter_chunks = re.finditer(SINGLE_DIGIT_INSTRUCTIONS_PATTERN_RE, instruction_text)
    for match_ in iter_chunks:
        variable_operands.append(
            VariableOperands(
                div_z=int(match_.group("div_z_operand")),
                add_x=int(match_.group("add_x_operand")),
                add_y=int(match_.group("add_y_operand")),
            )
        )
    assert len(variable_operands) == MODEL_NO_DIGITS
    return variable_operands


def execute_instructions(
    instructions: list[Instruction],
    inputs: list[int],
    variable_operands: VariableOperands,
    registers: Registers | FrozenRegisters | None = None,
) -> FrozenRegisters:
    if registers is None:
        registers = Registers()
    elif isinstance(registers, FrozenRegisters):
        registers = unfreeze_registers(registers)

    input_position_iter = itertools.count()

    for instruction in instructions:
        match instruction:
            case Instruction(Operator.INP, operand, _):
                input_position = next(input_position_iter)
                setattr(registers, operand, inputs[input_position])
            case Instruction(
                (
                    Operator.ADD
                    | Operator.MUL
                    | Operator.DIV
                    | Operator.MOD
                    | Operator.EQL
                ) as operator_,
                operand_1,
                operand_2,
            ):
                operation_fn = OPERATOR_FNS[operator_]
                operand_1_val = getattr(registers, operand_1)
                if isinstance(operand_2, RegisterAttr):
                    operand_2_val = getattr(registers, operand_2)
                elif isinstance(operand_2, VariableOperand):
                    operand_2_val = getattr(variable_operands, operand_2)
                else:
                    operand_2_val = operand_2
                result = operation_fn(operand_1_val, operand_2_val)
                setattr(registers, operand_1, result)
    return freeze_registers(registers)


class ModelNumberValidation:
    def __init__(self, instruction_text: str):
        self.single_digit_instructions = parse_single_digit_instructions()
        self.variable_operands = parse_variable_operands(instruction_text)
        self.chunk_positions = []
        for pos, var_op in enumerate(self.variable_operands):
            if var_op.add_x < 10:
                self.chunk_positions.append(pos)
        self.largest_model_number_range = range(9, 0, -1)
        self.smallest_model_number_range = range(1, 10)
        self._range = None

    def _validate_model_number(
        self, pos: int, digit: int, end_pos: int, registers: FrozenRegisters
    ) -> list[tuple[str, FrozenRegisters]]:
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
            result = self._validate_model_number(
                pos + 1, next_digit, end_pos, output_registers
            )
            if not result:
                continue

            for i in result:
                model_no_suffix, next_registers = i
                result_suffix = str(digit) + model_no_suffix

                results.append((result_suffix, next_registers))

        return results

    def validate_model_number_chunk(
        self,
        start_pos: int,
        chunk_pos: int,
        registers: FrozenRegisters = FrozenRegisters(),
    ) -> str | None:
        end_pos = self.chunk_positions[chunk_pos]
        results = {}
        for digit in self._range:
            result = self._validate_model_number(start_pos, digit, end_pos, registers)

            for i in result:
                model_no_suffix, output_registers = i
                if output_registers.z in results:
                    continue
                results[output_registers.z] = (model_no_suffix, output_registers)

        # base case
        if chunk_pos == len(self.chunk_positions) - 1:
            for z, (suffix, final_registers) in results.items():
                if z == 0:
                    return suffix
            return None

        # recursive case
        for next_model_no_prefix, next_register in results.values():
            suffix = self.validate_model_number_chunk(
                start_pos=end_pos + 1, chunk_pos=chunk_pos + 1, registers=next_register
            )
            if suffix is not None:
                return next_model_no_prefix + suffix

        return None

    def run(self, mode: Literal["smallest", "largest"]):
        self._range = (
            self.largest_model_number_range
            if mode == "largest"
            else self.smallest_model_number_range
        )
        result = self.validate_model_number_chunk(start_pos=0, chunk_pos=0)
        if result is None:
            raise ValueError("A result was not found")
        return result


def run():
    instruction_text = read_file()
    model_number_validation = ModelNumberValidation(instruction_text)
    print(model_number_validation.run(mode="largest"))
    print(model_number_validation.run(mode="smallest"))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
