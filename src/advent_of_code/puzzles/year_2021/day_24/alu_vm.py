import dataclasses
import enum
import itertools
import operator


class Operator(enum.StrEnum):
    INP = enum.auto()
    ADD = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()
    MOD = enum.auto()
    EQL = enum.auto()


class RegisterAttr(enum.StrEnum):
    W = enum.auto()
    X = enum.auto()
    Y = enum.auto()
    Z = enum.auto()


@dataclasses.dataclass(frozen=True)
class Instruction:
    operator: Operator
    operand_1: RegisterAttr
    operand_2: RegisterAttr | int | str | None


@dataclasses.dataclass
class Registers:
    w: int = 0
    x: int = 0
    y: int = 0
    z: int = 0


def eql_fn(a, b):
    return 1 if a == b else 0


OPERATOR_FNS = {
    Operator.ADD: operator.add,
    Operator.MUL: operator.mul,
    Operator.DIV: operator.floordiv,
    Operator.MOD: operator.mod,
    Operator.EQL: eql_fn,
}


def parse_instructions(instruction_text) -> list[Instruction]:
    instructions = []
    for raw_instruction in instruction_text.splitlines():
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
                        var_operand,
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


def execute_instructions(
    instructions: list[Instruction],
    inputs: list[int],
    variable_operands: dict[str, int] | None = None,
    registers: Registers | None = None,
) -> Registers:
    if registers is None:
        registers = Registers()

    # copy registers
    registers = dataclasses.replace(registers)

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
                elif isinstance(operand_2, str):
                    if variable_operands is None:
                        raise ValueError("expecting variable operands to be present")
                    operand_2_val = variable_operands[operand_2]
                else:
                    operand_2_val = operand_2
                result = operation_fn(operand_1_val, operand_2_val)
                setattr(registers, operand_1, result)
    return registers
