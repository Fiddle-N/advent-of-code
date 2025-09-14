import collections
import itertools
import PIL.Image
import PIL.ImageColor
import operator
import timeit


Coords = collections.namedtuple("Coords", "x y")


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


class IntCodeProgram(list):
    def _fill(self, key):
        extension = [0] * (key - len(self) + 1)
        self.extend(extension)

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except IndexError:
            self._fill(key)
            return super().__getitem__(key)

    def __setitem__(self, key, value):
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
        self.opcode = None
        self.input = [initial] if initial is not None else []
        self.output = []

    def get_next_output(self):
        next_output = self.output.pop(0)
        return next_output

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


# def number_of_panels(program):
#     colours = ['black', 'white']
#     angles = [-90, 90]
#
#     computer = IntCodeVM(program)
#     panels = set()
#     colour = 0
#     turtle.left(90)         # initialise turtle the correct way
#     while True:
#         panels.add(turtle.position())
#         state = computer.process(colour)
#         if state == 'end':
#             break
#         for colour, direction in grouper(computer.output, 2):
#             turtle.pencolor(colours[colour])
#             turtle.pendown()
#             turtle.penup()
#             turtle.right(angles[direction])
#             turtle.forward(1)
#             turtle.left(angles[direction])      # reorient up
#     return panels


def new_coord(coords, direction):
    directions = {
        "up": Coords(0, 1),
        "right": Coords(1, 0),
        "down": Coords(0, -1),
        "left": Coords(-1, 0),
    }
    change = directions[direction]
    return Coords(coords.x + change.x, coords.y + change.y)


def paint_hull_simulation(program, starting_colour=0):
    directions = ["up", "right", "down", "left"]

    computer = IntCodeVM(program)

    grid = {}
    position = Coords(0, 0)
    position_colour = starting_colour
    grid[position] = position_colour  # this could be dubious for panel number
    direction = 0
    while True:
        state = computer.process(position_colour)
        if state == "end":
            break
        colour_change = computer.get_next_output()
        direction_change_val = computer.get_next_output()
        assert not computer.output
        grid[position] = colour_change
        direction_change = 1 if direction_change_val else -1
        direction = (direction + direction_change) % len(directions)
        position = new_coord(position, directions[direction])
        position_colour = grid.get(position, 0)
    return grid


def shift_grid(grid):
    min_x = min(grid, key=lambda coords: coords.x).x
    min_y = min(grid, key=lambda coords: coords.y).y
    shifted_grid = {
        Coords(coords.x - min_x, coords.y - min_y): val for coords, val in grid.items()
    }
    min_shifted_x = min(shifted_grid, key=lambda coords: coords.x).x
    min_shifted_y = min(shifted_grid, key=lambda coords: coords.y).y
    assert min_shifted_x == 0
    assert min_shifted_y == 0
    return shifted_grid


def paint_picture(grid):
    colours = ["black", "white"]

    max_x = max(grid, key=lambda coords: coords.x).x
    max_y = max(grid, key=lambda coords: coords.y).y

    width = max_x + 1
    height = max_y + 1
    im = PIL.Image.new("1", (width, height))
    for x in range(width):
        for y in range(height):
            colour = grid.get(Coords(x, y), 0)
            im.putpixel((x, max_y - y), PIL.ImageColor.getcolor(colours[colour], "1"))
    im.save("output.png")


def main():
    program = read_file()

    print("emergency hull painting robot starting. Starting panel black")
    grid = paint_hull_simulation(program)
    print("emergency hull painting robot finished")
    print(f"number of panels printed once: {len(grid)}")
    print()

    print("emergency hull painting robot starting. Starting panel white")
    grid = paint_hull_simulation(program, starting_colour=1)
    print("emergency hull painting robot finished")
    shifted_grid = shift_grid(grid)
    paint_picture(shifted_grid)


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
