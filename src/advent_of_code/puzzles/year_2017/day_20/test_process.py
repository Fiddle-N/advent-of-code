from advent_of_code.puzzles.year_2017.day_20 import process


def test_closest_particle() -> None:
    raw_particles = """\
p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>"""
    particles = process.parse(raw_particles)
    assert process.closest_particle(particles) == 0


def calculate_remaining_after_collisions() -> None:
    raw_particles = """\
p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<1,0,0>, a=<0,0,0>"""
    particles = process.parse(raw_particles)
    assert process.calculate_remaining_after_collisions(particles) == 1


def test_calculate_remaining_after_collisions_non_zero_accel() -> None:
    raw_particles = """\
p=<2,0,0>, v=<1,0,0>, a=<1,0,0>
p=<-7,0,0>, v=<2,0,0>, a=<2,0,0>"""
    particles = process.parse(raw_particles)
    assert process.calculate_remaining_after_collisions(particles) == 0
