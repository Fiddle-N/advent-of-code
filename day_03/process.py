import timeit
import math

TREE = '#'


class TobogganTrajectory:

    def __init__(self, grid_str=None):
        grid_str = grid_str if grid_str is not None else self.read_input()
        self.grid = grid_str.split('\n')
        self.tree_coords = self.generate_tree_coords(self.grid)
        self.grid_rows = len(self.grid)
        self.grid_cols = len(self.grid[0])

    def read_input(self):
        with open('input.txt') as f:
            return f.read().strip()

    def generate_tree_coords(self, grid):
        tree_coords = set()
        for y, row in enumerate(grid):
            for x, space in enumerate(row):
                if space == TREE:
                    tree_coords.add((x, y))
        return tree_coords

    def calculate_trees_encountered(self, slope_x, slope_y):
        trees_encountered = 0
        step = 1
        while True:
            tobbogan_x = slope_x * step
            tobbogan_y = slope_y * step
            grid_x = tobbogan_x % self.grid_cols
            grid_y = tobbogan_y
            if (grid_x, grid_y) in self.tree_coords:
                trees_encountered += 1
            if grid_y < self.grid_rows - 1:
                step += 1
            else:
                return trees_encountered


def main():
    toboggan_trajectory = TobogganTrajectory()
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    trees_encountered = []
    for slope in slopes:
        slope_x, slope_y = slope
        trees = toboggan_trajectory.calculate_trees_encountered(slope_x, slope_y)
        print(f'Number of encountered trees for toboggan slope of right {slope_x}, down {slope_y}: {trees}')
        trees_encountered.append(trees)
    print(f'Final answer: {math.prod(trees_encountered)}')


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
