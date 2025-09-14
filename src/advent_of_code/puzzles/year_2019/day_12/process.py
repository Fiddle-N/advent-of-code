import collections
import itertools
import timeit
import dataclasses

import numpy as np

Coords = collections.namedtuple("Coords", "x y z")


@dataclasses.dataclass
class Moon:
    position: Coords
    velocity: Coords = Coords(0, 0, 0)

    @property
    def energy(self):
        return sum(abs(p) for p in self.position) * sum(abs(v) for v in self.velocity)


class Moons:
    def __init__(self, moons):
        self.moons = moons
        self.states = set()

    @property
    def total_energy(self):
        return sum(moon.energy for moon in self.moons)

    @staticmethod
    def _calculate_velocity_changes(positions):
        p0, p1 = positions
        if p0 < p1:
            return 1, -1
        elif p0 > p1:
            return -1, 1
        elif p0 == p1:
            return 0, 0
        else:
            raise Exception

    @staticmethod
    def _velocity_change(moon, change):
        x_change, y_change, z_change = change
        moon.velocity = Coords(
            moon.velocity.x + x_change,
            moon.velocity.y + y_change,
            moon.velocity.z + z_change,
        )

    def apply_gravity(self):
        for moon_0, moon_1 in itertools.combinations(self.moons, 2):
            positions = list(zip(moon_0.position, moon_1.position))
            velocity_change_for_positions = [
                self._calculate_velocity_changes(position) for position in positions
            ]
            velocity_change_for_moons = list(zip(*velocity_change_for_positions))
            moon_0_velocity_change, moon_1_velocity_change = velocity_change_for_moons
            self._velocity_change(moon_0, moon_0_velocity_change)
            self._velocity_change(moon_1, moon_1_velocity_change)

    def apply_velocity(self):
        for moon in self.moons:
            moon.position = Coords(
                moon.position.x + moon.velocity.x,
                moon.position.y + moon.velocity.y,
                moon.position.z + moon.velocity.z,
            )

    def _do_simulation(self):
        self.apply_gravity()
        self.apply_velocity()

        # if self.moons[0].position.y == 0 and self.moons[1].position.y == -10 and self.moons[2].position.y == -8 and self.moons[3].position.y == 5:
        #     print('hit on row 1 !', _)
        # if self.moons[0].position.x == -1 and self.moons[1].position.x == 2 and self.moons[2].position.x == 4 and self.moons[3].position.x == 3:
        #     print('hit on row 0 !', _)
        # if self.moons[0].position.z == 2 and self.moons[1].position.z == -7 and self.moons[2].position.z == 8 and self.moons[3].position.z == -1:
        #     print('hit on row 0 !', _)

    def simulate(self, time_steps=1):
        for time_step in range(1, time_steps + 1):
            self._do_simulation()

    def zipped_positions(self):
        positions = [moon.position for moon in self.moons]
        return zip(*positions)

    def zipped_velocities(self):
        velocities = [moon.velocity for moon in self.moons]
        return zip(*velocities)

    def first_repeat(self):
        time_step = 0
        x_vel_factor = y_vel_factor = z_vel_factor = None
        while x_vel_factor is None or y_vel_factor is None or z_vel_factor is None:
            self._do_simulation()
            time_step += 1
            x_velocity, y_velocity, z_velocity = self.zipped_velocities()
            if x_velocity == (0, 0, 0, 0) and x_vel_factor is None:
                x_vel_factor = time_step
            if y_velocity == (0, 0, 0, 0) and y_vel_factor is None:
                y_vel_factor = time_step
            if z_velocity == (0, 0, 0, 0) and z_vel_factor is None:
                z_vel_factor = time_step
        factors = [x_vel_factor, y_vel_factor, z_vel_factor]
        return np.lcm.reduce(factors, dtype="int64") * 2


def read_file():
    with open("input.txt") as f:
        return f.read().rstrip()


def process_text(text):
    moon_coords = []
    for coordinates in text.split("\n"):
        coordinates = coordinates.strip("<>")
        x, y, z = coordinates.split(",")
        _, x_value = x.split("=")
        _, y_value = y.split("=")
        _, z_value = z.split("=")
        moon_coords.append(
            Moon(
                Coords(
                    int(x_value),
                    int(y_value),
                    int(z_value),
                )
            )
        )
    return moon_coords


def main():
    text = read_file()
    moon_coords = process_text(text)
    moons = Moons(moon_coords)
    moons.simulate(1000)
    print(f"total energy after 1000 steps: {moons.total_energy}")

    moon_coords2 = process_text(text)
    moons2 = Moons(moon_coords2)
    first_repeat = moons2.first_repeat()
    print(f"first repeat after {first_repeat} steps")


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
