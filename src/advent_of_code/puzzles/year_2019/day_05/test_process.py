from advent_of_code.puzzles.year_2019.day_05 import process


def test_example():
    instructions = [int(x) for x in "3,9,8,9,10,9,4,9,99,-1,8".split(",")]
    program = process.OpCode(instructions, input=9)
    program.process()
    print("done")


# test_example()


def test_example_2():
    instructions = [int(x) for x in "3,9,7,9,10,9,4,9,99,-1,8".split(",")]
    program = process.OpCode(instructions, input=7)
    program.process()
    print("done")


# test_example_2()


def test_example_3():
    instructions = [int(x) for x in "3,3,1108,-1,8,3,4,3,99".split(",")]
    program = process.OpCode(instructions, input=9)
    program.process()
    print("done")


# test_example_3()


def test_example_4():
    instructions = [int(x) for x in "3,3,1107,-1,8,3,4,3,99".split(",")]
    program = process.OpCode(instructions, input=6)
    program.process()
    print("done")


# test_example_4()


def test_example_5():
    instructions = [
        int(x) for x in "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9".split(",")
    ]
    program = process.OpCode(instructions, input=-1)
    program.process()
    print("done")


# test_example_5()


def test_long_example():
    instructions = [
        int(x)
        for x in (
            "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
            + "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,"
            + "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
        ).split(",")
    ]
    program = process.OpCode(instructions, input=10)
    program.process()
    print("done")


test_long_example()
