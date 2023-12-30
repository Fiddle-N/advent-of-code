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


ONE_LEVEL_DROP = Coords3D(0, 0, -1)


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
                        (coord + ONE_LEVEL_DROP) in final_brick_coords
                        for coord in dropping_brick_coords
                    )
            ):
                break

            dropping_brick = Brick(
                dropping_brick.start + ONE_LEVEL_DROP,
                dropping_brick.end + ONE_LEVEL_DROP
            )

        final_bricks.append(dropping_brick)
        for coord in dropping_brick_coords:
            final_brick_coords[coord] = dropping_brick

    return final_bricks


