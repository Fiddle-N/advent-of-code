import dataclasses
import collections
import itertools
import math
import regex
import timeit

import more_itertools
import numpy as np


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int


class Grid:

    def __init__(self, grid):
        self.grid = grid

    def __len__(self):
        return len(self.grid)

    @property
    def top(self):
        return self.grid[0, :]

    @property
    def bottom(self):
        return self.grid[len(self) - 1, :]

    @property
    def left(self):
        return self.grid[:, 0]

    @property
    def right(self):
        return self.grid[:, len(self) - 1]

    def rotate(self):
        """Rotates clockwise 90"""
        self.grid = np.rot90(self.grid, -1)

    def flip(self):
        """Flips horizontally"""
        self.grid = np.fliplr(self.grid)

    def trim(self):
        borders = [(0, 0), (0, 1), (-1, 0), (-1, 1)]
        for obj, axis in borders:
            self.grid = np.delete(self.grid, obj, axis)


class JurassicJigsaw:

    OPPOSITES = {
        'top': 'bottom',
        'bottom': 'top',
        'left': 'right',
        'right': 'left',
    }

    DIRECTIONS = {
        'top': Coords(0, -1),
        'bottom': Coords(0, 1),
        'left': Coords(-1, 0),
        'right': Coords(1, 0),
    }

    SEA_MONSTER_PATTERN = [
        '..................#.',
        '#....##....##....###',
        '.#..#..#..#..#..#...',
    ]

    FULL_ROTATION = 4

    def __init__(self, tiles):
        self.tiles = tiles
        self.coords = {}
        self.process_tiles()
        self.picture = self._assemble_picture()

    @classmethod
    def from_text(cls, input_str):
        tiles = {}
        raw_tiles = input_str.split('\n\n')
        for raw_tile in raw_tiles:
            raw_label, raw_image = raw_tile.split('\n', maxsplit=1)
            label_re = regex.fullmatch(r'Tile (\d+):', raw_label)
            label = int(label_re.group(1))
            image = []
            for raw_row in raw_image.splitlines():
                row = list(raw_row)
                image.append(row)
            np_image = np.array(image)
            tiles[label] = Grid(np_image)
        return cls(tiles)

    @classmethod
    def from_file(cls):
        with open('input.txt') as f:
            return cls.from_text(f.read().strip())

    @property
    def grid(self):
        min_x = min(self.coords, key=lambda coords: coords.x).x
        max_x = max(self.coords, key=lambda coords: coords.x).x
        min_y = min(self.coords, key=lambda coords: coords.y).y
        max_y = max(self.coords, key=lambda coords: coords.y).y
        grid = []
        for y in range(min_y, max_y + 1):
            row = []
            for x in range(min_x, max_x + 1):
                row.append(self.coords.get(Coords(x, y)))
            grid.append(row)
        return grid

    @property
    def np_grid(self):
        np_grid = Grid(np.array(self.grid))
        return np_grid

    def _find_coords_for_label(self, label):
        for coords, label_name in self.coords.items():
            if label_name == label:
                return coords

    def _add_to_grid(self, label, other_label, direction):
        label_location = self._find_coords_for_label(label)
        directions_coords = self.DIRECTIONS[direction]
        new_location = Coords(label_location.x + directions_coords.x, label_location.y + directions_coords.y)
        self.coords[new_location] = other_label

    def _get_edge_configs(self):
        """Very naive at the moment - gets all edges instead of non matched. Hope and pray that there are no duplicate edges"""
        return list(itertools.product(self.coords.values(), self.DIRECTIONS))

    def process_tile(self, tile):
        label, image = tile
        if not len(self.coords):
            self.coords[Coords(0, 0)] = label
            return True
        edge_configs = self._get_edge_configs()
        for edge_config in edge_configs:
            assembled_label, side = edge_config
            other_side = self.OPPOSITES[side]
            edge = getattr(self.tiles[assembled_label], side)
            for turn_no in range(1, self.FULL_ROTATION * 2 + 1):
                other_edge = getattr(image, other_side)
                if (edge == other_edge).all():
                    self._add_to_grid(assembled_label, label, side)
                    return True
                image.rotate()
                if turn_no == self.FULL_ROTATION:
                    image.flip()
        return False

    def process_tiles(self):
        queue = collections.deque(self.tiles.items())
        while queue:
            tile = queue.popleft()
            success = self.process_tile(tile)
            if not success:
                queue.append(tile)

    def corner_tiles(self):
        corners = self.np_grid.grid[[0, 0, -1, -1], [0, -1, 0, -1]]
        return [int(corner) for corner in corners]

    def _assemble_picture(self):
        raw_picture = []
        for row in self.grid:
            row_arrays = [self.tiles[label] for label in row]
            for tile in row_arrays:
                tile.trim()
            raw_arrays = [tile.grid for tile in row_arrays]
            concat_arrays = np.concatenate(raw_arrays, axis=1)
            raw_picture.append(concat_arrays)
        return Grid(np.concatenate(raw_picture, axis=0))

    @staticmethod
    def _find_sea_monsters_in_single_orientation(image, regex_mode):
        image = [''.join(row) for row in image]
        if regex_mode == 'chunked':
            matches = 0
            for rows in more_itertools.windowed(image, 3):
                window_iters = [more_itertools.windowed(row, 20) for row in rows]
                for section in zip(*window_iters):
                    section_str = [''.join(line) for line in section]
                    pattern_line = zip(JurassicJigsaw.SEA_MONSTER_PATTERN, section_str)
                    if all(regex.fullmatch(pattern, line) for pattern, line in pattern_line):
                        matches += 1
            return matches
        elif regex_mode == 'full':
            image_str = '\n'.join(image)
            len_pattern = len(JurassicJigsaw.SEA_MONSTER_PATTERN[0])
            spaces_between_rows = '.{{{}}}'.format(len(image) - len_pattern + 1)
            pattern = f'{spaces_between_rows}'.join(JurassicJigsaw.SEA_MONSTER_PATTERN)
            return len(regex.findall(pattern, image_str, flags=regex.DOTALL, overlapped=True))

    def find_sea_monsters(self, regex_mode='full'):
        for turn_no in range(1, self.FULL_ROTATION * 2 + 1):
            if monsters := self._find_sea_monsters_in_single_orientation(self.picture.grid, regex_mode):
                return monsters
            self.picture.rotate()
            if turn_no == self.FULL_ROTATION:
                self.picture.flip()

    def water_roughness(self):
        sea_monster_number = self.find_sea_monsters()
        sea_monster_weight = sum(body_part.count('#') for body_part in self.SEA_MONSTER_PATTERN)
        total_sea_monster_weight = sea_monster_number * sea_monster_weight
        water_roughness_plus_sea_monsters = np.count_nonzero(self.picture.grid == '#')
        return water_roughness_plus_sea_monsters - total_sea_monster_weight


def main():
    jurassic_jigsaw = JurassicJigsaw.from_file()
    corner_tiles = jurassic_jigsaw.corner_tiles()
    print(f'Corner tiles: {corner_tiles}')
    print(f'Corner tiles product: {math.prod(corner_tiles)}')
    print(f"Sea monsters: {jurassic_jigsaw.find_sea_monsters()}")
    print(f'Water roughness: {jurassic_jigsaw.water_roughness()}')


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')

