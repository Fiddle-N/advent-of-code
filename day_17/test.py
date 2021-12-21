from day_17 import process


def test():
    target_area = 'target area: x=20..30, y=-10..-5'
    trick_shot = process.TrickShot(target_area)

    assert trick_shot.y_peak() == 45

    initial_velocities = trick_shot.initial_velocities()
    assert len(initial_velocities) == 112
    assert initial_velocities == {
        (23, -10),
        (25, -7),
        (8, 0),
        (26, -10),
        (20, -8),
        (25, -6),
        (25, -10),
        (8, 1),
        (24, -10),
        (7, 5),
        (23, -5),
        (27, -10),
        (8, -2),
        (25, -9),
        (26, -6),
        (30, -6),
        (7, -1),
        (13, -2),
        (15, -4),
        (7, 8),
        (22, -8),
        (23, -8),
        (23, -6),
        (24, -8),
        (7, 2),
        (27, -8),
        (27, -5),
        (25, -5),
        (29, -8),
        (7, 7),
        (7, 3),
        (9, -2),
        (11, -3),
        (13, -4),
        (30, -8),
        (28, -10),
        (27, -9),
        (30, -9),
        (30, -5),
        (29, -6),
        (6, 8),
        (20, -10),
        (8, -1),
        (28, -8),
        (15, -2),
        (26, -7),
        (7, 6),
        (7, 0),
        (10, -2),
        (30, -7),
        (21, -8),
        (24, -7),
        (22, -6),
        (11, -2),
        (6, 7),
        (21, -9),
        (29, -9),
        (12, -2),
        (7, 1),
        (28, -6),
        (9, -1),
        (11, -1),
        (28, -5),
        (22, -7),
        (21, -7),
        (20, -5),
        (6, 4),
        (6, 2),
        (15, -3),
        (28, -9),
        (23, -9),
        (11, -4),
        (10, -1),
        (20, -9),
        (21, -10),
        (24, -9),
        (9, 0),
        (29, -10),
        (6, 1),
        (20, -7),
        (22, -5),
        (12, -3),
        (6, 0),
        (12, -4),
        (26, -5),
        (14, -2),
        (7, 9),
        (20, -6),
        (27, -7),
        (6, 3),
        (14, -4),
        (30, -10),
        (26, -8),
        (24, -6),
        (22, -10),
        (26, -9),
        (22, -9),
        (29, -7),
        (6, 6),
        (6, 9),
        (24, -5),
        (28, -7),
        (21, -6),
        (14, -3),
        (25, -8),
        (23, -7),
        (27, -6),
        (7, 4),
        (6, 5),
        (13, -3),
        (21, -5),
        (29, -5),
    }
