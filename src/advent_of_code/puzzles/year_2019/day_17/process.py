import operator

from advent_of_code.common import Coords


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
        self._program = IntCodeProgram(
            int(instruction) for instruction in program.split(",")
        )
        self._instruction_pointer = 0
        self._relative_base = 0
        self._current_opcode: str
        self.input = [initial] if initial is not None else []
        self.output = []

    def put(self, input_val):
        if not isinstance(input_val, list):
            input_val = list(input_val)
        self.input.extend(input_val)

    def get(self):
        next_output = self.output.pop(0)
        return next_output

    def change_memory(self, address, value):
        self._program[address] = value

    def _read_param(self, offset_index):
        mode = int(self._current_opcode[-(offset_index + 2)])
        address = self._program[self._instruction_pointer + offset_index]
        if mode == 0:
            param = self._program[address]
        elif mode == 1:
            param = address
        elif mode == 2:
            param = self._program[self._relative_base + address]
        else:
            raise Exception
        return param

    def _write_param(self, offset_index, value):
        mode = int(self._current_opcode[-(offset_index + 2)])
        address = self._program[self._instruction_pointer + offset_index]
        if mode == 0:
            self._program[address] = value
        elif mode == 2:
            self._program[self._relative_base + address] = value
        else:
            raise Exception

    def _process_three_params(self, operation):
        param1 = self._read_param(1)
        param2 = self._read_param(2)
        value = operation(param1, param2)
        self._write_param(3, int(value))
        self._instruction_pointer += 4

    def _write_input(self):
        if self.input:
            next_input = self.input.pop(0)
            self._write_param(1, next_input)
            self._instruction_pointer += 2
            return True
        else:
            return False

    def _read_output(self):
        self.output.append(self._read_param(1))
        self._instruction_pointer += 2

    def _change_relative_base(self):
        param = self._read_param(1)
        self._relative_base += param
        self._instruction_pointer += 2

    def _change_pointer(self, reverse=False):
        param1 = self._read_param(1)
        param2 = self._read_param(2)
        if reverse:
            param1 = not param1
        if param1:
            self._instruction_pointer = param2
        else:
            self._instruction_pointer += 3

    def process(self):
        while True:
            self._current_opcode = str(self._program[self._instruction_pointer]).zfill(
                5
            )
            instruction = self._current_opcode[-2:]
            if instruction == "99":
                return "end"
            if instruction == "01":
                self._process_three_params(operator.add)
            if instruction == "02":
                self._process_three_params(operator.mul)
            if instruction == "03":
                written = self._write_input()
                if not written:
                    return "waiting for input"
            if instruction == "04":
                self._read_output()
            if instruction == "05":
                self._change_pointer(reverse=False)
            if instruction == "06":
                self._change_pointer(reverse=True)
            if instruction == "07":
                self._process_three_params(operator.lt)
            if instruction == "08":
                self._process_three_params(operator.eq)
            if instruction == "09":
                self._change_relative_base()


def read_file():
    with open("input.txt") as f:
        return f.read().rstrip()


class AsciiAlignmentParam:
    DIRECTIONS = [
        Coords(0, -1),
        Coords(0, 1),
        Coords(1, 0),
        Coords(-1, 0),
    ]

    def __init__(self, program):
        ascii_computer = IntCodeVM(program)
        ascii_computer.process()
        self.output_str = "".join(chr(char) for char in ascii_computer.output)
        self.output = [list(row) for row in self.output_str.rstrip().split("\n")]
        self.details = self._generate_details()

    def _generate_details(self):
        details = {
            Coords(x, y): space
            for y, row in enumerate(self.output)
            for x, space in enumerate(row)
        }
        return details

    def _is_alignment_param(self, position):
        space = self.details[position]
        if space != "#":
            return False
        surrounding_positions = [position + direction for direction in self.DIRECTIONS]
        for position in surrounding_positions:
            if self.details.get(position) != "#":
                return False
        return True

    def sum(self):
        alignment_params = [
            position for position in self.details if self._is_alignment_param(position)
        ]
        return sum(position.x * position.y for position in alignment_params)


def convert_to_ascii_codepoints(text):
    result = [ord(char) for char in text]
    return result


def ascii_robot_manoeuvre(program):
    ascii_computer = IntCodeVM(program)
    ascii_computer.change_memory(address=0, value=2)

    main_movement_routine = "A,B,A,B,A,C,A,C,B,C\n"
    movement_function_a = "R,6,L,10,R,10,R,10\n"
    movement_function_b = "L,10,L,12,R,10\n"
    movement_function_c = "R,6,L,12,L,10\n"
    continuous_video_feed = "n\n"
    inputs = [
        main_movement_routine,
        movement_function_a,
        movement_function_b,
        movement_function_c,
        continuous_video_feed,
    ]
    ascii_inputs = []
    for inpt in inputs:
        assert len(inpt) <= 21
        ascii_inputs.append(convert_to_ascii_codepoints(inpt))

    for inpt in ascii_inputs:
        ascii_computer.process()
        ascii_computer.put(inpt)

    for x in ascii_computer.output:
        print(chr(x), end="")
        if x == 962913:
            print(x)
    # while True:
    #     print(ascii_computer.get())


def main():
    # program = read_file()
    # asc = AsciiAlignmentParam(program)
    # print(asc.output_str)
    # print('Sum of alignment params:', asc.sum())

    program = read_file()
    print("Amount of dust:", ascii_robot_manoeuvre(program))


if __name__ == "__main__":
    main()
