import operator
import timeit


class IntCodeProgram(list):
    def _fill(self, key):
        extension = [0] * (key - len(self) + 1)
        self.extend(extension)

    def __getitem__(self, key):  # ty: ignore[invalid-method-override]
        try:
            return super().__getitem__(key)
        except IndexError:
            self._fill(key)
            return super().__getitem__(key)

    def __setitem__(self, key, value):  # ty: ignore[invalid-method-override]
        try:
            super().__setitem__(key, value)
        except IndexError:
            self._fill(key)
            super().__setitem__(key, value)


class IntCodeVM:
    def __init__(self, program, initial=None):
        self.program = IntCodeProgram(
            int(instruction) for instruction in program.rstrip().split(",")
        )
        self.instruction_pointer = 0
        self.relative_base = 0
        self.opcode: str
        self.input = [initial] if initial is not None else []
        self.output = []

    def read_param(self, offset_index):
        mode = int(self.opcode[-(offset_index + 2)])
        address = self.program[self.instruction_pointer + offset_index]
        if mode == 0:
            param = self.program[address]
        elif mode == 1:
            param = address
        elif mode == 2:
            param = self.program[self.relative_base + address]
        else:
            raise Exception
        return param

    def write_param(self, offset_index, value):
        mode = int(self.opcode[-(offset_index + 2)])
        address = self.program[self.instruction_pointer + offset_index]
        if mode == 0:
            self.program[address] = value
        elif mode == 2:
            self.program[self.relative_base + address] = value
        else:
            raise Exception

    def process_three_params(self, operation):
        param1 = self.read_param(1)
        param2 = self.read_param(2)
        value = operation(param1, param2)
        self.write_param(3, int(value))
        self.instruction_pointer += 4

    def write_input(self):
        if self.input:
            next_input = self.input.pop(0)
            self.write_param(1, next_input)
            self.instruction_pointer += 2
            return True
        else:
            return False

    def read_output(self):
        self.output.append(self.read_param(1))
        self.instruction_pointer += 2

    def change_relative_base(self):
        param = self.read_param(1)
        self.relative_base += param
        self.instruction_pointer += 2

    def change_pointer(self, reverse=False):
        param1 = self.read_param(1)
        param2 = self.read_param(2)
        if reverse:
            param1 = not param1
        if param1:
            self.instruction_pointer = param2
        else:
            self.instruction_pointer += 3

    def process(self, input_val=None):
        if input_val is not None:
            self.input.append(input_val)
        while True:
            self.opcode = str(self.program[self.instruction_pointer]).zfill(5)
            instruction = self.opcode[-2:]
            if instruction == "99":
                return "end"
            if instruction == "01":
                self.process_three_params(operator.add)
            if instruction == "02":
                self.process_three_params(operator.mul)
            if instruction == "03":
                written = self.write_input()
                if not written:
                    return "waiting for input"
            if instruction == "04":
                self.read_output()
            if instruction == "05":
                self.change_pointer(reverse=False)
            if instruction == "06":
                self.change_pointer(reverse=True)
            if instruction == "07":
                self.process_three_params(operator.lt)
            if instruction == "08":
                self.process_three_params(operator.eq)
            if instruction == "09":
                self.change_relative_base()


def read_file():
    with open("input.txt") as f:
        return f.read()


def main():
    program = read_file()

    test_computer = IntCodeVM(program, initial=1)
    print("BOOST program test mode initiated")
    print("BOOST program test mode: running program")
    test_computer.process()
    for code in test_computer.output:
        print(code)
    print("BOOST program test mode complete")
    print()

    sensor_boost_computer = IntCodeVM(program, initial=2)
    print("BOOST program sensor boost mode initiated")
    print("BOOST program sensor boost mode: running program")
    sensor_boost_computer.process()
    for code in sensor_boost_computer.output:
        print(code)
    print("Boost program sensor boost mode complete")
    print()


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
