import operator


class OpCode:
    def __init__(self, instructions, input=1):
        self.program = instructions
        self.input = input
        self.address = 0
        self.opcode: str

    def retrieve_param(self, relative_index):
        mode = int(self.opcode[-(relative_index + 2)])
        param_address = self.program[self.address + relative_index]
        param = param_address if mode else self.program[param_address]
        return param

    def write_param(self, relative_index, value):
        self.program[self.program[self.address + relative_index]] = value

    def process_three_params(self, operation):
        param1 = self.retrieve_param(1)
        param2 = self.retrieve_param(2)
        value = operation(param1, param2)
        self.write_param(3, int(value))
        self.address += 4

    def process_one_param(self, mode):
        if mode == "write":
            self.write_param(1, self.input)
        if mode == "read":
            param = self.retrieve_param(1)
            print(param)
        self.address += 2

    def change_pointer(self, reverse=False):
        param1 = self.retrieve_param(1)
        param2 = self.retrieve_param(2)
        if reverse:
            param1 = not param1
        if param1:
            self.address = param2
        else:
            self.address += 3

    def process(self):
        while True:
            self.opcode = str(self.program[self.address]).zfill(5)
            instruction = self.opcode[-2:]
            if instruction == "99":
                return
            if instruction == "01":
                self.process_three_params(operator.add)
            if instruction == "02":
                self.process_three_params(operator.mul)
            if instruction == "03":
                self.process_one_param(mode="write")
            if instruction == "04":
                self.process_one_param(mode="read")
            if instruction == "05":
                self.change_pointer(reverse=False)
            if instruction == "06":
                self.change_pointer(reverse=True)
            if instruction == "07":
                self.process_three_params(operator.lt)
            if instruction == "08":
                self.process_three_params(operator.eq)


def read_file():
    with open("input.txt") as f:
        return [int(opcode) for opcode in f.read().rstrip().split(",")]


def main():
    diagnostic_test = read_file()

    print("air con diagnostic test:")
    air_con = OpCode(diagnostic_test.copy(), input=1)
    air_con.process()
    print("air con diagnostic test done")

    print()

    print("thermal radiator diagnostic test:")
    thermal_radiator = OpCode(diagnostic_test.copy(), input=5)
    thermal_radiator.process()
    print("thermal radiator diagnostic test done")


if __name__ == "__main__":
    main()
