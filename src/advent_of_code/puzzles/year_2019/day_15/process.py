import itertools
import operator
import dataclasses
import timeit


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


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

    def _read_param(self, offset_index):
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

    def _write_param(self, offset_index, value):
        mode = int(self.opcode[-(offset_index + 2)])
        address = self.program[self.instruction_pointer + offset_index]
        if mode == 0:
            self.program[address] = value
        elif mode == 2:
            self.program[self.relative_base + address] = value
        else:
            raise Exception

    def process_three_params(self, operation):
        param1 = self._read_param(1)
        param2 = self._read_param(2)
        value = operation(param1, param2)
        self._write_param(3, int(value))
        self.instruction_pointer += 4

    def _write_input(self):
        if self.input:
            next_input = self.input.pop(0)
            self._write_param(1, next_input)
            self.instruction_pointer += 2
            return True
        else:
            return False

    def _read_output(self):
        self.output.append(self._read_param(1))
        self.instruction_pointer += 2

    def _change_relative_base(self):
        param = self._read_param(1)
        self.relative_base += param
        self.instruction_pointer += 2

    def _change_pointer(self, reverse=False):
        param1 = self._read_param(1)
        param2 = self._read_param(2)
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
                self.process_three_params(operator.lt)
            if instruction == "08":
                self.process_three_params(operator.eq)
            if instruction == "09":
                self._change_relative_base()


def read_file():
    with open("input.txt") as f:
        return f.read().rstrip()


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        return Coords(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other):
        return Coords(
            self.x - other.x,
            self.y - other.y,
        )


@dataclasses.dataclass
class Node:
    distance_from_start: int
    previous_node: Coords | None = None
    is_oxygen_system: bool = False


class RepairDroid:
    DIRECTIONS = ("N", "S", "W", "E")

    DIRECTION_COORDINATES = {
        "N": Coords(0, -1),
        "S": Coords(0, 1),
        "E": Coords(1, 0),
        "W": Coords(-1, 0),
    }

    COORDINATES_DIRECTIONS = {
        value: key for key, value in DIRECTION_COORDINATES.items()
    }

    def __init__(self, program):
        self.computer = IntCodeVM(program)
        start = Coords(0, 0)
        self.droid = start
        self.open_list = []
        self.oxygen_system = None
        self.details = {}

    @property
    def droid_node(self):
        return self.details[self.droid]

    def _new_location(self, location, direction):
        change = self.DIRECTION_COORDINATES[direction]
        new_location = location + change
        return new_location

    def _attempt_move_droid_in_direction(self, direction):
        directions = (None, "N", "S", "W", "E")
        computer_input = directions.index(direction)
        state = self.computer.process(computer_input)
        assert state == "waiting for input"
        output = self.computer.get_next_output()
        return output

    def _move_droid_in_direction(self, direction, track=False):
        output = self._attempt_move_droid_in_direction(direction)
        new_location = self._new_location(self.droid, direction)
        if output in (1, 2):
            distance_from_start = self.droid_node.distance_from_start + 1
            if track and (
                new_location not in self.details
                or distance_from_start < self.details[new_location].distance_from_start
            ):
                self.details[new_location] = Node(
                    distance_from_start=distance_from_start,
                    previous_node=self.droid,
                    is_oxygen_system=True if output == 2 else False,
                )
                self.open_list.append(new_location)
            self.droid = new_location
            did_move = True
        elif output == 0:
            did_move = False
        else:
            raise Exception
        return did_move

    def _uncover_square(self, direction="N"):
        opposite_directions = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E",
        }
        movable_to = self._move_droid_in_direction(direction, track=True)
        if movable_to:
            self._move_droid_in_direction(opposite_directions[direction], track=True)
        return movable_to

    def _backtrack_to_start(self, position):
        path = [position]
        while True:
            node = self.details[position]
            position = node.previous_node
            if position is None:
                break
            path.append(position)
        return path

    @staticmethod
    def _path_to_path(path, other_path):
        path_segment = []

        for node in path:
            path_segment.append(node)
            if node in other_path:
                common_node = node
                break

        other_path_segment = []
        for node in other_path:
            other_path_segment.append(node)
            if node == common_node:
                break

        reversed_other_path_segment = list(reversed(other_path_segment))
        common_path = path_segment + reversed_other_path_segment[1:]
        return common_path

    def _move_droid_to_position(self, position):
        if self.droid == position:
            return
        current_path_to_start = self._backtrack_to_start(self.droid)
        other_path_to_start = self._backtrack_to_start(position)
        path = self._path_to_path(current_path_to_start, other_path_to_start)
        coord_directions = [next - previous for previous, next in pairwise(path)]
        directions = [
            self.COORDINATES_DIRECTIONS[coords] for coords in coord_directions
        ]
        for direction in directions:
            did_move = self._move_droid_in_direction(direction, track=False)
            assert did_move

    def find_oxygen_system_node(self):
        for coords, node in self.details.items():
            if node.is_oxygen_system:
                self.oxygen_system = coords

    def map_maze(self, start=Coords(0, 0), reset=False):
        if start != self.droid:
            self._move_droid_to_position(start)
        if reset:
            self.open_list = []
            self.details = {}
        self.open_list.append(start)
        self.details[start] = Node(distance_from_start=0)
        while self.open_list:
            next_position = self.open_list.pop(0)
            self._move_droid_to_position(next_position)
            for direction in self.DIRECTIONS:
                self._uncover_square(direction)

    def shortest_path_to_oxygen(self):
        oxygen_system_node = self.details[self.oxygen_system]
        return oxygen_system_node.distance_from_start

    def furthest_from_start(self):
        furthest_distance = max(
            self.details.values(), key=lambda node: node.distance_from_start
        ).distance_from_start
        return furthest_distance


def main():
    program = read_file()
    rd = RepairDroid(program)
    rd.map_maze()
    rd.find_oxygen_system_node()
    print(
        "Shortest distance from start to oxygen system:", rd.shortest_path_to_oxygen()
    )
    rd.map_maze(start=rd.oxygen_system, reset=True)
    print("Time for oxygen to fill room:", rd.furthest_from_start())


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
