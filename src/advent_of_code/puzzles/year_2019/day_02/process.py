import itertools
import timeit


class OpCode:
    def __init__(self):
        self.instructions = []

    def read_file(self):
        with open("input.txt") as f:
            self.instructions = [int(opcode) for opcode in f.read().rstrip().split(",")]

    def process(self, input1=None, input2=None):
        instructions = self.instructions.copy()
        if input1 is not None:
            instructions[1] = input1
        if input2 is not None:
            instructions[2] = input2
        while True:
            for address in itertools.count(start=0, step=4):
                opcode = instructions[address]
                if opcode == 99:
                    return instructions[0]
                if opcode in (1, 2):
                    parameter_1_address = instructions[address + 1]
                    parameter_2_address = instructions[address + 2]
                    parameter_3_address = instructions[address + 3]
                    if opcode == 1:
                        instructions[parameter_3_address] = (
                            instructions[parameter_1_address]
                            + instructions[parameter_2_address]
                        )
                    if opcode == 2:
                        instructions[parameter_3_address] = (
                            instructions[parameter_1_address]
                            * instructions[parameter_2_address]
                        )

    def find_output(self, number):
        for noun, verb in itertools.product(range(100), range(100)):
            output = self.process(noun, verb)
            if output and (output == number):
                return noun, verb
        print("not found")


def main():
    opc = OpCode()
    opc.read_file()
    result = opc.process(12, 2)
    print(f"position 0: {result}")
    noun, verb = opc.find_output(19690720)
    print(f"100 * noun + verb for result 19690720: {100 * noun + verb}")


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
