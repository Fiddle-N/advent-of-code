import dataclasses
import functools
import enum
import itertools
import operator
import re

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
        self.num_26 = len(
            [
                variable_operand
                for variable_operand in self.variable_operands
                if variable_operand.div_z == 26
            ]
        )
        print()

    @functools.cache
    def _validate_model_number(
        self, model_no_pos: int, digit: int, registers: FrozenRegisters, num_26
    ) -> tuple[str, FrozenRegisters, int] | None:
        var_ops = self.variable_operands[model_no_pos]

        if var_ops.div_z == 26:
            num_26 -= 1

        output_registers = execute_instructions(
            self.single_digit_instructions,
            [digit],
            var_ops,
            registers,
        )

        is_x_0 = output_registers.x == 0

        # base case
        if model_no_pos == (MODEL_NO_DIGITS - 1):
            return str(digit), output_registers, is_x_0

            # if output_registers.z == 0:
            #     return str(digit), output_registers, is_x_0
            # return None

        # if output_registers.z >= (26 ** num_26):
        #     return None

        # recursive case
        for next_digit in range(9, 0, -1):
            print(model_no_pos)
            result = self._validate_model_number(
                model_no_pos + 1, next_digit, output_registers, num_26
            )
            # print(self._validate_model_number.cache_info())
            # if result is None:
            #     continue
            model_no_suffix, next_registers, next_is_x_0 = result

            result_suffix = str(digit) + model_no_suffix

            if (result_is_x_0 := (is_x_0 + next_is_x_0)) == self.num_26:
                raise ValueError(result_suffix)

            # print(f"{result_is_x_0=}")

            # return (result_suffix, output_registers, result_is_x_0)

        return None

    def validate_model_number(self) -> str:
        for digit in range(9, 0, -1):
            result = self._validate_model_number(
                model_no_pos=0,
                digit=digit,
                registers=freeze_registers(Registers()),
                num_26=self.num_26,
            )
            # if result is None:
            #     continue
            # model_no_suffix, _, __ = result
            # return str(digit) + model_no_suffix
        raise RuntimeError("a result must be present")


def run():
    instruction_text = read_file()
    model_number_validation = ModelNumberValidation(instruction_text)
    print(model_number_validation.validate_model_number())


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
