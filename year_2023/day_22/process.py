import collections
import dataclasses


@dataclasses.dataclass(frozen=True)
class Coords3D:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Coords3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )


ONE_LEVEL_ABOVE = Coords3D(0, 0, 1)
ONE_LEVEL_BELOW = Coords3D(0, 0, -1)


@dataclasses.dataclass(frozen=True)
class Brick:
    start: Coords3D
    end: Coords3D

    def coords(self):
        coords = [
            Coords3D(x, y, z)
            for z in range(self.start.z, self.end.z + 1)
            for y in range(self.start.y, self.end.y + 1)
            for x in range(self.start.x, self.end.x + 1)
        ]
        return coords


def read_file() -> str:
    with open("input.txt") as f:
        return f.read()


def parse(input_):
    bricks = []
    for brick_input in input_.splitlines():
        start_input, end_input = brick_input.split('~')
        start_ints = [int(val) for val in start_input.split(',')]
        end_ints = [int(val) for val in end_input.split(',')]
        start = Coords3D(*start_ints)
        end = Coords3D(*end_ints)
        assert start.x <= end.x and start.y <= end.y and start.z <= end.z
        brick = Brick(start, end)
        bricks.append(brick)
    return bricks


def falling_bricks(bricks: list[Brick]):
    # sort bricks by height, using the lowest part of brick as base
    sorted_bricks = sorted(bricks, key=lambda brick: brick.start.z)

    final_bricks = []
    final_brick_coords = {}

    for brick in sorted_bricks:

        dropping_brick = brick
        while True:
            dropping_brick_coords = dropping_brick.coords()
            if (
                    # brick is on the ground
                    dropping_brick.start.z == 1

                    # brick is resting on another brick
                    or any(
                (coord + ONE_LEVEL_BELOW) in final_brick_coords
                        for coord in dropping_brick_coords
                    )
            ):
                break

            dropping_brick = Brick(
                dropping_brick.start + ONE_LEVEL_BELOW,
                dropping_brick.end + ONE_LEVEL_BELOW
            )

        final_bricks.append(dropping_brick)
        for coord in dropping_brick_coords:
            final_brick_coords[coord] = dropping_brick

    return final_bricks, final_brick_coords


def brick_dependency_hierarchy(bricks, bricks_coords):
    hierarchy = {}
    for brick in bricks:
        coords = brick.coords()
        highest_z = brick.end.z
        highest_coords = [
            coord
            for coord in coords
            if coord.z == highest_z
        ]
        one_level_up = [
            (coord + ONE_LEVEL_ABOVE)
            for coord in highest_coords
        ]
        resting_bricks = {
            bricks_coords[coord]
            for coord in one_level_up
            if coord in bricks_coords
        }
        hierarchy[brick] = resting_bricks
    return hierarchy


def hierarchical_dependent_count(hierarchy, dependent_count):
    hierarchy_dependent_count = {}
    for brick, dependents in hierarchy.items():
        brick_dependent_count = [
            dependent_count[brick]
            for brick in dependents
        ]
        hierarchy_dependent_count[brick] = brick_dependent_count
    return hierarchy_dependent_count


def disintegrable_bricks(hierarchy):
    dependent_count = collections.Counter()
    for bricks in hierarchy.values():
        dependent_count.update(bricks)

    hierarchy_dependent_count = hierarchical_dependent_count(
        hierarchy, dependent_count
    )

    disintegrable = []
    not_disintegrable = []
    for brick, counts in hierarchy_dependent_count.items():
        if (
                # no bricks are dependent on this brick
                not counts

                # TODO add test where changing all to any would fail test
                # all bricks are dependent on more than one brick
                or all(count > 1 for count in counts)
        ):
            disintegrable.append(brick)
        else:
            not_disintegrable.append(brick)

    return disintegrable, not_disintegrable


def main():
    input_ = read_file()

    bricks = parse(input_)
    fallen_bricks, fallen_brick_coords = falling_bricks(bricks)
    hierarchy = brick_dependency_hierarchy(fallen_bricks, fallen_brick_coords)
    disintegrable, not_disintegrable = disintegrable_bricks(hierarchy)

    print(
        f"Number of safely disintegrable bricks:",
        len(disintegrable),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
