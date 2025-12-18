import collections
import itertools
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
            int(instruction) for instruction in program.split(",")
        )
        self.instruction_pointer = 0
        self.relative_base = 0
        self.opcode: str
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
        return f.read().rstrip()


def block_tiles(text):
    arcade = IntCodeVM(text)
    arcade.process()
    tiles = {}
    icons = ["▢", "▣", "▩", "▤", "◉"]
    for instruction in grouper(arcade.output, 3):
        x, y, tile = instruction
        tiles[Coords(x, y)] = icons[tile]
    max_x = max(tiles, key=lambda coords: coords.x).x
    max_y = max(tiles, key=lambda coords: coords.y).y
    columns = max_x + 1
    rows = max_y + 1
    grid = [[tiles[Coords(x, y)] for x in range(columns)] for y in range(rows)]
    for row in grid:
        print("".join(row))
    block_tiles_coords = [
        coords for coords, tile in tiles.items() if icons.index(tile) == 2
    ]
    return len(block_tiles_coords)


def play_game(text):
    arcade = IntCodeVM(text)
    arcade.program[0] = 2
    input_val = None
    while True:
        state = arcade.process(input_val)
        tiles = {}
        icons = ["▢", "▣", "▩", "▤", "◉"]
        score = 0
        for instruction in grouper(arcade.output, 3):
            x, y, tile = instruction
            if tile == 3:
                player = Coords(x, y)
            if tile == 4:
                ball = Coords(x, y)
            if (x, y) == (-1, 0):
                score = tile
            else:
                tiles[Coords(x, y)] = icons[tile]
        if state == "end":
            return score
        # max_x = max(tiles, key=lambda coords: coords.x).x
        # max_y = max(tiles, key=lambda coords: coords.y).y
        # columns = max_x + 1
        # rows = max_y + 1
        # # grid = [
        #     [tiles[Coords(x, y)] for x in range(columns)]
        #     for y in range(rows)
        # ]
        # for row in grid:
        #     print(''.join(row))
        # print()
        # print('Score', score)
        if player.x > ball.x:
            input_val = -1
        elif player.x < ball.x:
            input_val = 1
        elif player.x == ball.x:
            input_val = 0
        else:
            raise Exception
        # time.sleep(0.25)


def main():
    text = read_file()
    block_tile_no = block_tiles(text)
    print(f"block tile number: {block_tile_no}")

    print(play_game(text))


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
