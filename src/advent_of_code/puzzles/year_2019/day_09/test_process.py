from advent_of_code.puzzles.year_2019.day_09 import process


def test_example_1():
    input_text = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    computer = process.IntCodeVM(input_text)
    computer.process()
    output_text = ",".join(str(x) for x in computer.output)
    assert input_text == output_text


def test_example_2():
    input_text = "1102,34915192,34915192,7,4,7,99,0"
    computer = process.IntCodeVM(input_text)
    computer.process()
    assert len(str(computer.output[0])) == 16


def test_example_3():
    input_text = "104,1125899906842624,99"
    computer = process.IntCodeVM(input_text)
    computer.process()
    assert computer.output[0] == 1125899906842624
