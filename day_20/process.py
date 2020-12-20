import dataclasses
import collections
import itertools
import math
import regex as re
import timeit

import more_itertools
import numpy as np


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int


class Tile:

    def __init__(self, tile):
        self.tile = tile
        self.length = len(tile)

    @property
    def top(self):
        return self.tile[0, :]

    @property
    def bottom(self):
        return self.tile[self.length - 1, :]

    @property
    def left(self):
        return self.tile[:, 0]

    @property
    def right(self):
        return self.tile[:, self.length - 1]

    def rotate(self):
        """Rotates clockwise 90"""
        self.tile = np.rot90(self.tile, -1)

    def flip(self):
        """Flips horizontally"""
        self.tile = np.fliplr(self.tile)

    def trim(self):
        self.tile = np.delete(self.tile, 0, 0)
        self.tile = np.delete(self.tile, 0, 1)
        self.tile = np.delete(self.tile, -1, 0)
        self.tile = np.delete(self.tile, -1, 1)


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

    def __init__(self, input_str):
        self.tiles = self._preprocess(input_str)
        self.matches = {}
        self.coords = {}
        self.process_tiles()
        self.assemble_picture()

    @staticmethod
    def _preprocess(input_str):
        tiles = {}
        raw_tiles = input_str.split('\n\n')
        for raw_tile in raw_tiles:
            raw_label, raw_image = raw_tile.split('\n', maxsplit=1)
            label_re = re.fullmatch(r'Tile (\d+):', raw_label)
            label = int(label_re.group(1))
            image = []
            for raw_row in raw_image.splitlines():
                row = list(raw_row)
                image.append(row)
            np_image = np.array(image)
            tiles[label] = Tile(np_image)
        return tiles

    @classmethod
    def from_file(cls):
        with open('input.txt') as f:
            return cls(f.read().strip())

    def _add_to_grid(self, label, other_label, direction):
        for coords, label_name in self.coords.items():
            if label_name == label:
                label_location = coords
                break
        else:
            raise Exception
        directions_coords = self.DIRECTIONS[direction]
        new_location = Coords(label_location.x + directions_coords.x, label_location.y + directions_coords.y)
        self.coords[new_location] = other_label

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
        np_grid = Tile(np.array(self.grid))
        return np_grid

    def _get_non_matched_edges(self):
        """Very naive at the moment - actually gets all edges instead of non matched. Hope and pray that there are no duplicate edges"""
        return list(itertools.product(self.coords.values(), self.DIRECTIONS))

    def _process_tile(self, tile):
        label, image = tile

        non_matched_edges = self._get_non_matched_edges()

        for non_matched in non_matched_edges:
            match_label, side = non_matched
            other_side = self.OPPOSITES[side]
            edge = getattr(self.tiles[match_label], side)
            for _ in range(4):
                other_edge = getattr(image, other_side)
                if (edge == other_edge).all():
                    self._add_to_grid(match_label, label, side)
                    return True
                else:
                    image.rotate()
            image.flip()
            for _ in range(4):
                other_edge = getattr(image, other_side)
                if (edge == other_edge).all():
                    self._add_to_grid(match_label, label, side)
                    return True
                else:
                    image.rotate()
        # no matches
        return False

    def process_tile(self, tile):
        label, image = tile
        if not len(self.coords):
            self.coords[Coords(0, 0)] = label
            return True
        else:
            return self._process_tile(tile)

    def process_tiles(self):
        queue = collections.deque(self.tiles.items())
        while queue:
            tile = queue.popleft()
            success = self.process_tile(tile)
            if not success:
                queue.append(tile)

    def corner_tiles(self):
        corners = self.np_grid.tile[[0, 0, -1, -1], [0, -1, 0, -1]]
        return [int(corner) for corner in corners]

    @staticmethod
    def _find_sea_monsters(image, regex_mode):
        image = [''.join(row) for row in image]
        if regex_mode == 'chunked':
            matches = 0
            for rows in more_itertools.windowed(image, 3):
                window_iters = [more_itertools.windowed(row, 20) for row in rows]
                for section in zip(*window_iters):
                    section_str = [''.join(line) for line in section]
                    pattern_line = zip(JurassicJigsaw.SEA_MONSTER_PATTERN, section_str)
                    match = all(re.fullmatch(pattern, line) for pattern, line in pattern_line)
                    if match:
                        matches += 1
            return matches
        elif regex_mode == 'full':
            image_str = '\n'.join(image)
            len_pattern = len(JurassicJigsaw.SEA_MONSTER_PATTERN[0])
            spaces_between_rows = '.{{{}}}'.format(len(image) - len_pattern + 1)
            pattern = f'{spaces_between_rows}'.join(JurassicJigsaw.SEA_MONSTER_PATTERN)
            return len(re.findall(pattern, image_str, flags=re.DOTALL, overlapped=True))

    def assemble_picture(self):
        raw_picture = []
        for row in self.grid:
            row_arrays = [self.tiles[label] for label in row]
            for tile in row_arrays:
                tile.trim()
            raw_arrays = [tile.tile for tile in row_arrays]
            concat_arrays = np.concatenate(raw_arrays, axis=1)
            raw_picture.append(concat_arrays)
        self.picture = Tile(np.concatenate(raw_picture, axis=0))

    def find_sea_monsters(self, regex_mode='full'):
        for _ in range(4):
            monsters = self._find_sea_monsters(self.picture.tile, regex_mode)
            if monsters:
                return monsters
            else:
                self.picture.rotate()
        self.picture.flip()
        for _ in range(4):
            monsters = self._find_sea_monsters(self.picture.tile, regex_mode)
            if monsters:
                return monsters
            else:
                self.picture.rotate()

    def water_roughness(self):
        sea_monster_number = self.find_sea_monsters()
        sea_monster_weight = sum(body_part.count('#') for body_part in self.SEA_MONSTER_PATTERN)
        total_sea_monster_weight = sea_monster_number * sea_monster_weight
        water_roughness_plus_sea_monsters = np.count_nonzero(self.picture.tile == '#')
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

