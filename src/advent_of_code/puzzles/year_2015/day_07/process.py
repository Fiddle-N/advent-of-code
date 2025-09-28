import operator
from collections.abc import Callable
from typing import Literal
import functools

from advent_of_code.common import read_file, timed_run


GATE_OPERATIONS = {
    "AND": operator.and_,
    "OR": operator.or_,
    "LSHIFT": operator.lshift,
    "RSHIFT": operator.rshift,
}

type CircuitFn = Callable[[], int]
type Circuit = dict[str, CircuitFn]


def not_16(x: int) -> int:
    return (~x) & 0xFFFF


def resolve_operand(circuit: Circuit, operand: str):
    try:
        val_1 = int(operand)
    except ValueError:
        val_1 = circuit[operand]()
    return val_1


def input_execute_factory(circuit: Circuit, op_1: str) -> CircuitFn:
    @functools.cache
    def execute() -> int:
        return resolve_operand(circuit, op_1)

    return execute


def inverse_execute_factory(circuit: Circuit, op_1: str) -> CircuitFn:
    @functools.cache
    def execute() -> int:
        return not_16(resolve_operand(circuit, op_1))

    return execute


def binary_op_execute_factory(
    circuit: Circuit,
    op_1: str,
    op_2: str,
    gate: Literal["AND", "OR", "LSHIFT", "RSHIFT"],
) -> CircuitFn:
    @functools.cache
    def execute() -> int:
        return GATE_OPERATIONS[gate](
            resolve_operand(circuit, op_1), resolve_operand(circuit, op_2)
        )

    return execute


def assemble_circuit(circuit_text) -> Circuit:
    circuit: Circuit = {}
    for entry in circuit_text.splitlines():
        operation, wire = entry.split(" -> ")
        match operation.split():
            case [op_1]:
                circuit[wire] = input_execute_factory(circuit, op_1)
            case ["NOT", op_1]:
                circuit[wire] = inverse_execute_factory(circuit, op_1)
            case [op_1, ("AND" | "OR" | "LSHIFT" | "RSHIFT") as gate, op_2]:
                circuit[wire] = binary_op_execute_factory(circuit, op_1, op_2, gate)

    return circuit


def override_circuit(circuit: Circuit, wire: str, value: int) -> None:
    @functools.cache
    def execute() -> int:
        return value

    circuit[wire] = execute


def run() -> None:
    circuit_text = read_file()

    circuit = assemble_circuit(circuit_text)
    wire_a_value = circuit["a"]()
    print(wire_a_value)

    circuit = assemble_circuit(circuit_text)
    override_circuit(circuit, "b", wire_a_value)
    wire_a_value = circuit["a"]()
    print(wire_a_value)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
