import pytest

from advent_of_code.puzzles.year_2021.day_24 import alu_vm


def test_alu_negate_value_program():
    alu_program = """\
inp x
mul x -1"""
    instructions = alu_vm.parse_instructions(alu_program)
    output = alu_vm.execute_instructions(instructions=instructions, inputs=[4])
    assert output.x == -4


@pytest.mark.parametrize(
    "input_, exp_z",
    [
        ([3, 9], 1),
        ([3, 8], 0),
    ],
)
def test_alu_check_number_multiplied_by_three_program(input_, exp_z):
    alu_program = """\
inp z
inp x
mul z 3
eql z x"""
    instructions = alu_vm.parse_instructions(alu_program)
    output = alu_vm.execute_instructions(instructions=instructions, inputs=input_)
    assert output.z == exp_z


def test_alu_binary_converter_program():
    alu_program = """\
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""
    instructions = alu_vm.parse_instructions(alu_program)
    output = alu_vm.execute_instructions(instructions=instructions, inputs=[7])
    assert output.w == 0
    assert output.x == 1
    assert output.y == 1
    assert output.z == 1
