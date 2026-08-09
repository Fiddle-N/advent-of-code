"""
2017 Day 20

https://adventofcode.com/2017/day/20

Part 1
The particle that stays closest to <0,0,0> is simply that with the smallest
magnitude acceleration.

Part 2
The equation for the location of a point is
p + (v + a) + (v + 2a) + (v + 3a) + ...

Simplified down, this is
p_t = p_0 + vt + a Σ(i = 1 to t)i

The closed form of a summation Σ(i = 1 to x)i is simply (x(x+1)) / 2

So, simplified down further, the closed form of the location equation is
p_t = p_0 + vt + (1/2)t(t+1)a

Expanded out to remove the denominator, this equals
p_t = 1/2 (2p_0 + 2vt + t(t+1)a)
p_t = 1/2 (2p_0 + 2vt + a(t^2) + at)
p_t = 1/2 (a(t^2) + (2v + a)t + 2p_0)

For pairs of particles, we can simply work this out for each axis, subtracting
one equation from the other to get an equation in the form ax^2 + bx + c = 0,
which we can then use the quadratic formula to solve to work out the time values
that the particles will collide at for that axis. Note, if a is 0, the solution
is linear; if b is also 0, then there is either infinitely many solutions for the
axis if the two cs are equal, else no solutions.

Once this is calculated, we can combine across axes for each pair of points to
work out actual collisions, then collide particles for increasing time values
to calculate the particles that will remain.
"""

import itertools
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from typing import Literal

from advent_of_code.common import BaseCoords, Coords, quad_formula, read_file, timed_run


SIGNED_INT_PATTERN = r"-?\d+"
PARTICLE_PATTERN = (
    rf"p=<(?P<p_x>{SIGNED_INT_PATTERN}),(?P<p_y>{SIGNED_INT_PATTERN}),(?P<p_z>{SIGNED_INT_PATTERN})>, "
    rf"v=<(?P<v_x>{SIGNED_INT_PATTERN}),(?P<v_y>{SIGNED_INT_PATTERN}),(?P<v_z>{SIGNED_INT_PATTERN})>, "
    rf"a=<(?P<a_x>{SIGNED_INT_PATTERN}),(?P<a_y>{SIGNED_INT_PATTERN}),(?P<a_z>{SIGNED_INT_PATTERN})>"
)


@dataclass(frozen=True, order=True)
class Position(BaseCoords):
    pass


@dataclass(frozen=True, order=True)
class Velocity(BaseCoords):
    pass


@dataclass(frozen=True, order=True)
class Acceleration(BaseCoords):
    pass


@dataclass(frozen=True)
class ParticleAxis:
    position: int
    velocity: int
    acceleration: int


@dataclass(frozen=True)
class Particle:
    position: Position
    velocity: Velocity
    acceleration: Acceleration

    @cache
    def to_axis(self, axis: Literal["x", "y", "z"]) -> ParticleAxis:
        return ParticleAxis(
            position=getattr(self.position, axis),
            velocity=getattr(self.velocity, axis),
            acceleration=getattr(self.acceleration, axis),
        )


def parse(raw_particles: str) -> list[Particle]:
    particles = []
    for raw_particle in raw_particles.splitlines():
        match = re.fullmatch(PARTICLE_PATTERN, raw_particle)
        assert match
        particles.append(
            Particle(
                Position(int(match["p_x"]), int(match["p_y"]), int(match["p_z"])),
                Velocity(int(match["v_x"]), int(match["v_y"]), int(match["v_z"])),
                Acceleration(int(match["a_x"]), int(match["a_y"]), int(match["a_z"])),
            )
        )
    return particles


def closest_particle(particles: list[Particle]) -> int:
    return min(
        enumerate(particles),
        key=lambda particle_pair: particle_pair[1].acceleration.manhattan_distance_to(
            Coords(0, 0, 0)
        ),
    )[0]


def _will_collide_axis(
    particle_0: Particle, particle_1: Particle, axis: Literal["x", "y", "z"]
) -> set[float] | None:
    # utilises quadratic formula

    particle_axis_0 = particle_0.to_axis(axis)
    particle_axis_1 = particle_1.to_axis(axis)

    qf_0_a = particle_axis_0.acceleration
    qf_0_b = 2 * particle_axis_0.velocity + particle_axis_0.acceleration
    qf_0_c = 2 * particle_axis_0.position

    qf_1_a = particle_axis_1.acceleration
    qf_1_b = 2 * particle_axis_1.velocity + particle_axis_1.acceleration
    qf_1_c = 2 * particle_axis_1.position

    qf_a = qf_1_a - qf_0_a
    qf_b = qf_1_b - qf_0_b
    qf_c = qf_1_c - qf_0_c

    if qf_a != 0:
        # quadratic
        return quad_formula(qf_a, qf_b, qf_c)
    elif qf_b != 0:
        # linear
        return {-qf_c / qf_b}
    elif qf_c == 0:
        # non-moving particles in the same axis location - infinitely many solutions
        return None
    else:
        # non-moving particles in different axis locations - no solutions
        return set()


def _will_collide(particle_0: Particle, particle_1: Particle) -> set[float]:
    collision_axes = []
    for axis in ("x", "y", "z"):
        axis_collision = _will_collide_axis(particle_0, particle_1, axis)
        if axis_collision is not None:
            collision_axes.append(axis_collision)
    collisions = set.intersection(*collision_axes)
    return collisions


def _calculate_collisions(
    particles: list[Particle],
) -> dict[tuple[Particle, Particle], set[float]]:
    collisions = {}
    for particle_0, particle_1 in itertools.combinations(particles, 2):
        particle_collisions = _will_collide(particle_0, particle_1)
        if particle_collisions:
            collisions[(particle_0, particle_1)] = particle_collisions
    return collisions


def _validate_and_transpose_collisions(
    collisions: dict[tuple[Particle, Particle], set[float]],
) -> dict[int, set[Particle]]:
    # validate and transpose
    transposed_collisions = defaultdict(set)
    for pair, pair_collisions in collisions.items():
        for collision in pair_collisions:
            if not collision.is_integer():
                continue
            for particle in pair:
                transposed_collisions[int(collision)].add(particle)
    return transposed_collisions


def _resolve_collisions(
    particles: list[Particle], collisions: dict[int, set[Particle]]
) -> set[Particle]:
    sorted_collisions = {time: collisions[time] for time in sorted(collisions)}
    particle_set = set(particles)
    for time, time_collisions in sorted_collisions.items():
        # only collide particles if all particles are still present
        if particle_set & time_collisions == time_collisions:
            particle_set -= time_collisions
    return particle_set


def calculate_remaining_after_collisions(particles: list[Particle]):
    collisions = _calculate_collisions(particles)
    transposed_collisions = _validate_and_transpose_collisions(collisions)
    remaining_particles = _resolve_collisions(particles, transposed_collisions)
    return len(remaining_particles)


def run():
    raw_particles = read_file()
    particles = parse(raw_particles)
    print(closest_particle(particles))
    print(calculate_remaining_after_collisions(particles))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
