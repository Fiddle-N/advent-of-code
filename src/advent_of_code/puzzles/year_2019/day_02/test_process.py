from advent_of_code.puzzles.year_2019.day_02 import process  # not working


def test_example_1():
    opc = process.OpCode()
    opc.instructions = [1, 0, 0, 0, 99]
    result = opc.process()
    assert result == 2


# def test_example_2():
#     opc = process.OpCode()
#     opc.instructions = [2, 3, 0, 3, 99]
#     instructions = opc.process()
#     assert instructions[3] == 6
#
#
# def test_example_3():
#     opc = process.OpCode()
#     opc.instructions = [2, 4, 4, 5, 99, 0]
#     instructions = opc.process()
#     assert instructions[5] == 9801


def test_example_4():
    opc = process.OpCode()
    opc.instructions = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    rename = opc.process()
    assert rename == 30
