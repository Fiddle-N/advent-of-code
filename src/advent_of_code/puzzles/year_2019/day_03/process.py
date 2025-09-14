import collections
import timeit

Direction = collections.namedtuple("Direction", "coordinate change")


class CrossedWires:
    START = (0, 0)
    DIRECTIONS = {
        "U": Direction(1, 1),
        "R": Direction(0, 1),
        "D": Direction(1, -1),
        "L": Direction(0, -1),
    }

    def __init__(self, path1=None, path2=None):
        self.path1 = path1
        self.path2 = path2
        self.coords1 = None
        self.coords2 = None
        self.steps1 = None
        self.steps2 = None
        self.intersections = None

    def read_file(self):
        with open("input.txt") as f:
            text = f.readlines()
            self.path1 = text[0].split(",")
            self.path2 = text[1].split(",")

    def _find_coordinates(self, path):
        coords = set()
        steps = {}
        current_location = list(self.START)
        total_distance = 0
        for part_path in path:
            direction = part_path[:1]
            distance = int(part_path[1:])
            for step in range(distance):
                coordinate, change = self.DIRECTIONS[direction]
                current_location[coordinate] += change
                current_location_hashable = tuple(current_location)
                coords.add(current_location_hashable)
                total_distance += 1
                if current_location_hashable not in steps:
                    steps[current_location_hashable] = total_distance
        return coords, steps

    def calculate_coords_and_steps(self):
        self.coords1, self.steps1 = self._find_coordinates(self.path1)
        self.coords2, self.steps2 = self._find_coordinates(self.path2)

    def find_closest_intersection(self):
        self.intersections = self.coords1.intersection(self.coords2)
        distances = [abs(x) + abs(y) for x, y in self.intersections]
        return min(distances)

    def find_fewest_combined_steps(self):
        intersection_steps = [
            self.steps1[step] + self.steps2[step] for step in self.intersections
        ]
        return min(intersection_steps)


def main():
    cw = CrossedWires()
    cw.read_file()
    cw.calculate_coords_and_steps()
    closest_intersection_distance = cw.find_closest_intersection()
    print(f"Closest intersection distance: {closest_intersection_distance}")
    fewest_combined_steps = cw.find_fewest_combined_steps()
    print(f"Fewest combined steps: {fewest_combined_steps}")


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
