import itertools
import operator
import timeit


class IntCode:
    def __init__(self, program, initial):
        self.program = [int(instruction) for instruction in program.rstrip().split(",")]
        self.instruction_pointer = 0
        self.opcode = None
        self.input = [initial]
        self.output = None

    def retrieve_param(self, relative_index):
        mode = int(self.opcode[-(relative_index + 2)])
        param_address = self.program[self.instruction_pointer + relative_index]
        if mode == 0:
            param = self.program[param_address]
        elif mode == 1:
            param = param_address
        else:
            raise Exception
        return param

    def write_param(self, relative_index, value):
        self.program[self.program[self.instruction_pointer + relative_index]] = value

    def process_three_params(self, operation):
        param1 = self.retrieve_param(1)
        param2 = self.retrieve_param(2)
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
        self.output = self.retrieve_param(1)
        self.instruction_pointer += 2

    def change_pointer(self, reverse=False):
        param1 = self.retrieve_param(1)
        param2 = self.retrieve_param(2)
        if reverse:
            param1 = not param1
        if param1:
            self.instruction_pointer = param2
        else:
            self.instruction_pointer += 3

    def process(self, input):
        self.input.append(input)
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


def _run_cycle(amplifiers, feedback_loop):
    io = 0
    state = None
    while True:
        for amplifier in amplifiers:
            state = amplifier.process(io)
            io = amplifier.output
        if not feedback_loop or state == "end":
            return amplifiers[-1].output


def highest_signal(program, phase_values=range(5), feedback_loop=False):
    signals = []
    for phases in itertools.permutations(phase_values, len(phase_values)):
        amplifiers = [IntCode(program, phase) for phase in phases]
        signal = _run_cycle(amplifiers, feedback_loop)
        signals.append(signal)
    return max(signals)


def read_file():
    with open("input.txt") as f:
        return f.read()


def main():
    program = read_file()

    max_signal = highest_signal(program)
    print(f"Highest signal: {max_signal}")

    max_signal = highest_signal(program, phase_values=range(5, 10), feedback_loop=True)
    print(f"Highest signal with feedback loop: {max_signal}")


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
