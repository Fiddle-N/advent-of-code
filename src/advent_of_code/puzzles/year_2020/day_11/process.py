import collections
import timeit

import more_itertools


EMPTY = 'L'
OCCUPIED = '#'

Coords = collections.namedtuple('Coords', 'x y')


DIRECTIONS = {
    'up': Coords(0, 1),
    'right-up': Coords(1, 1),
    'right': Coords(1, 0),
    'right-down': Coords(1, -1),
    'down': Coords(0, -1),
    'left-down': Coords(-1, -1),
    'left': Coords(-1, 0),
    'left-up': Coords(-1, 1),
}


class SeatingSystem:

    def __init__(self, grid_str=None):
        grid_str = grid_str if grid_str is not None else self._read_file()
        grid = [list(line) for line in grid_str.splitlines()]
        self.row_no = len(grid[0])
        self.col_no = len(grid)
        self.grid = set()
        self.seats = {}
        for y, row in enumerate(grid):
            for x, space in enumerate(row):
                space_position = Coords(x, y)
                self.grid.add(space_position)
                if space in (EMPTY, OCCUPIED):
                    self.seats[space_position] = space

    @staticmethod
    def _read_file():
        with open('input.txt') as f:
            return f.read()

    def output_grid(self, seats):
        grid = [['.' for _ in range(self.row_no)] for _ in range(self.col_no)]
        for seat_coords, seat in seats.items():
            grid[seat_coords.y][seat_coords.x] = seat
        return SeatingSystem._to_str(grid)

    @staticmethod
    def _to_str(input_list):
        return '\n'.join([''.join(row) for row in input_list])


class AbstractSeatingSystemModel:

    def __init__(self, seating_system):
        self.grid = seating_system.grid
        self.seats = seating_system.seats.copy()
        self.adj_seats = {seat: self.surrounding_seats(seat) for seat in self.seats}

    def __iter__(self):
        return self

    def __next__(self):
        current_seats = self.seats
        self.seats = {}
        for seat_coords, seat in current_seats.items():
            adj_seat_coords = self.adj_seats[seat_coords]
            adj_seats = collections.Counter(current_seats[adj_seat] for adj_seat in adj_seat_coords)
            if seat == EMPTY and not adj_seats.get(OCCUPIED, 0):
                self.seats[seat_coords] = OCCUPIED
            elif seat == OCCUPIED and adj_seats.get(OCCUPIED, 0) >= self.unacceptable_occupied_seats:
                self.seats[seat_coords] = EMPTY
            else:
                self.seats[seat_coords] = seat
        return self.seats

    @property
    def unacceptable_occupied_seats(self):
        """Override to specify the minimum number of occupied surrounding seats to make a seat vacant """
        raise NotImplementedError

    def surrounding_seats(self, coords):
        """Override to specify the surrounding seats that are considered from one seat"""
        raise NotImplementedError


class TheoreticalSeatingSystemModel(AbstractSeatingSystemModel):

    @property
    def unacceptable_occupied_seats(self):
        return 4

    def surrounding_seats(self, coords):
        next_coords = []
        for direction in DIRECTIONS.values():
            next_coord = Coords(coords.x + direction.x, coords.y + direction.y)
            if next_coord in self.seats:
                next_coords.append(next_coord)
        return next_coords


class RealSeatingSystemModel(AbstractSeatingSystemModel):

    @property
    def unacceptable_occupied_seats(self):
        return 5

    def surrounding_seats(self, coords):
        next_coords = []
        for direction in DIRECTIONS.values():
            start_coords = coords
            while True:
                next_coord = Coords(start_coords.x + direction.x, start_coords.y + direction.y)
                if next_coord in self.seats:
                    next_coords.append(next_coord)
                    break
                elif next_coord not in self.grid:
                    break
                start_coords = next_coord
        return next_coords



def _run_model(model):
    for current_seats, next_seats in more_itertools.windowed(model, 2):
        if current_seats == next_seats:
            return current_seats


def run_model(model, grid_str=None):
    seating_system = SeatingSystem(grid_str)
    primed_model = model(seating_system)
    current_seats = _run_model(primed_model)
    results = collections.Counter(current_seats.values())
    return results[OCCUPIED]


def main():
    print(f'Occupied seats in completed theoretical model: {run_model(TheoreticalSeatingSystemModel)}')
    print(f'Occupied seats in completed real model: {run_model(RealSeatingSystemModel)}')


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
