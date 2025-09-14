import collections
import decimal
import math
import timeit

Coords = collections.namedtuple("Coords", "x y")


def read_file():
    with open("input.txt") as f:
        return f.read()


def grid(text):
    return [list(row) for row in text.rstrip().split("\n")]


def get_asteroids(region):
    asteroids = []
    for y, row in enumerate(region):
        for x, position in enumerate(row):
            if position == "#":
                asteroids.append(Coords(x, y))
    return asteroids


def get_distances(current_asteroid, other_asteroids):
    return [
        Coords(asteroid.x - current_asteroid.x, asteroid.y - current_asteroid.y)
        for asteroid in other_asteroids
    ]


def remove_division_by_zero_trap():
    con = decimal.getcontext()
    con.traps[decimal.DivisionByZero] = False


def in_line_of_sight(distances):
    remove_division_by_zero_trap()
    angles = [
        (
            (decimal.Decimal(distance.y) / decimal.Decimal(distance.x)),
            math.copysign(1, distance.x),
            math.copysign(1, distance.y),
        )
        for distance in distances
    ]
    seen_asteroids = 0
    while angles:
        current_angle = angles.pop()
        if current_angle not in angles:
            seen_asteroids += 1
    return seen_asteroids


def get_best_location(asteroids):
    seen_asteroids = []
    for current_asteroid in asteroids:
        other_asteroids = [
            asteroid for asteroid in asteroids if asteroid != current_asteroid
        ]
        distances = get_distances(current_asteroid, other_asteroids)
        seen_asteroids_for_current_asteroid = in_line_of_sight(distances)
        seen_asteroids.append(seen_asteroids_for_current_asteroid)
    asteroids_with_seen_values = zip(asteroids, seen_asteroids)
    return max(asteroids_with_seen_values, key=lambda x: x[1])


def clockwise(current_asteroid, asteroids):
    other_asteroids = [
        asteroid for asteroid in asteroids if asteroid != current_asteroid
    ]
    distances = get_distances(current_asteroid, other_asteroids)
    angle_distance = []
    for distance, actual_coord in zip(distances, other_asteroids):
        distance_from_asteroid = math.sqrt(distance.x**2 + distance.y**2)
        angle = math.degrees(math.atan2(distance.y, distance.x))
        if angle < 0:
            angle += 360
        angle = (360 - angle) % 360
        angle = (angle - 90) % 360
        angle = (360 - angle) % 360
        angle_distance.append((distance, angle, distance_from_asteroid, actual_coord))
    return angle_distance


def calculate_true_angle(angle_distances):
    angles = {angle_distance[1] for angle_distance in angle_distances}
    true_angles = []
    for angle in angles:
        matching_angles = [
            angle_distance
            for angle_distance in angle_distances
            if angle_distance[1] == angle
        ]
        sorted_angles = sorted(matching_angles, key=lambda x: x[2])
        true_angles_for_current_angle = [
            (angle_distance[0], angle_distance[1] + (360 * idx), angle_distance[3])
            for idx, angle_distance in enumerate(sorted_angles)
        ]
        true_angles.extend(true_angles_for_current_angle)
    sorted_true_angles = sorted(true_angles, key=lambda x: x[1])
    return sorted_true_angles


def two_hundred_asteroid(sorted_true_angles):
    return sorted_true_angles[199][2]


def main():
    text = read_file()
    region = grid(text)
    asteroids = get_asteroids(region)
    best_location = get_best_location(asteroids)
    print(f"best location: {best_location[0]}")
    print(f"best location number of asteroids: {best_location[1]}")

    angle_distances = clockwise(best_location[0], asteroids)
    sorted_true_angles = calculate_true_angle(angle_distances)
    correct_asteroid = two_hundred_asteroid(sorted_true_angles)
    print(f"200th asteroid: {correct_asteroid}")


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
