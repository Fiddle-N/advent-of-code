import pytest

from year_2023.day_22 import process


@pytest.mark.parametrize(
    "brick_input",
    [
        # pre-sorted input
        """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""",
        """\
2,0,5~2,2,5
0,0,2~2,0,2
0,0,4~0,2,4
0,1,6~2,1,6
0,2,3~2,2,3
1,0,1~1,2,1
1,1,8~1,1,9""",
    ],
    ids=["presorted_input", "unsorted_input"],
)
def test_falling_bricks(brick_input):
    bricks = process.parse(brick_input)
    fallen_bricks, fallen_brick_coords = process.falling_bricks(bricks)
    assert fallen_bricks == [
        process.Brick(
            process.Coords3D(1, 0, 1),
            process.Coords3D(1, 2, 1),
        ),
        process.Brick(
            process.Coords3D(0, 0, 2),
            process.Coords3D(2, 0, 2),
        ),
        process.Brick(
            process.Coords3D(0, 2, 2),
            process.Coords3D(2, 2, 2),
        ),
        process.Brick(
            process.Coords3D(0, 0, 3),
            process.Coords3D(0, 2, 3),
        ),
        process.Brick(
            process.Coords3D(2, 0, 3),
            process.Coords3D(2, 2, 3),
        ),
        process.Brick(
            process.Coords3D(0, 1, 4),
            process.Coords3D(2, 1, 4),
        ),
        process.Brick(
            process.Coords3D(1, 1, 5),
            process.Coords3D(1, 1, 6),
        ),
    ]

    hierarchy = process.brick_dependency_hierarchy(fallen_bricks, fallen_brick_coords)
    assert hierarchy == {
        process.Brick(
            process.Coords3D(1, 0, 1),
            process.Coords3D(1, 2, 1),
        ): {
            process.Brick(
                process.Coords3D(0, 0, 2),
                process.Coords3D(2, 0, 2),
            ),
            process.Brick(
                process.Coords3D(0, 2, 2),
                process.Coords3D(2, 2, 2),
            ),
        },
        process.Brick(
            process.Coords3D(0, 0, 2),
            process.Coords3D(2, 0, 2),
        ): {
            process.Brick(
                process.Coords3D(0, 0, 3),
                process.Coords3D(0, 2, 3),
            ),
            process.Brick(
                process.Coords3D(2, 0, 3),
                process.Coords3D(2, 2, 3),
            ),
        },
        process.Brick(
            process.Coords3D(0, 2, 2),
            process.Coords3D(2, 2, 2),
        ): {
            process.Brick(
                process.Coords3D(0, 0, 3),
                process.Coords3D(0, 2, 3),
            ),
            process.Brick(
                process.Coords3D(2, 0, 3),
                process.Coords3D(2, 2, 3),
            ),
        },
        process.Brick(
            process.Coords3D(0, 0, 3),
            process.Coords3D(0, 2, 3),
        ): {
            process.Brick(
                process.Coords3D(0, 1, 4),
                process.Coords3D(2, 1, 4),
            ),
        },
        process.Brick(
            process.Coords3D(2, 0, 3),
            process.Coords3D(2, 2, 3),
        ): {
            process.Brick(
                process.Coords3D(0, 1, 4),
                process.Coords3D(2, 1, 4),
            ),
        },
        process.Brick(
            process.Coords3D(0, 1, 4),
            process.Coords3D(2, 1, 4),
        ): {
            process.Brick(
                process.Coords3D(1, 1, 5),
                process.Coords3D(1, 1, 6),
            ),
        },
        process.Brick(
            process.Coords3D(1, 1, 5),
            process.Coords3D(1, 1, 6),
        ): set(),
    }
    dependent_count = process.calculate_dependent_count(hierarchy)
    disintegrable, not_disintegrable = process.disintegrable_bricks(
        hierarchy, dependent_count
    )
    assert disintegrable == [
        process.Brick(
            process.Coords3D(0, 0, 2),
            process.Coords3D(2, 0, 2),
        ),
        process.Brick(
            process.Coords3D(0, 2, 2),
            process.Coords3D(2, 2, 2),
        ),
        process.Brick(
            process.Coords3D(0, 0, 3),
            process.Coords3D(0, 2, 3),
        ),
        process.Brick(
            process.Coords3D(2, 0, 3),
            process.Coords3D(2, 2, 3),
        ),
        process.Brick(
            process.Coords3D(1, 1, 5),
            process.Coords3D(1, 1, 6),
        ),
    ]
    assert len(disintegrable) == 5

    chain_reaction_fallen_bricks = process.chain_reaction(
        hierarchy, dependent_count, structural_bricks=not_disintegrable
    )

    assert chain_reaction_fallen_bricks == {
        process.Brick(
            process.Coords3D(1, 0, 1),
            process.Coords3D(1, 2, 1),
        ): {
            process.Brick(
                process.Coords3D(0, 0, 2),
                process.Coords3D(2, 0, 2),
            ),
            process.Brick(
                process.Coords3D(0, 2, 2),
                process.Coords3D(2, 2, 2),
            ),
            process.Brick(
                process.Coords3D(0, 0, 3),
                process.Coords3D(0, 2, 3),
            ),
            process.Brick(
                process.Coords3D(2, 0, 3),
                process.Coords3D(2, 2, 3),
            ),
            process.Brick(
                process.Coords3D(0, 1, 4),
                process.Coords3D(2, 1, 4),
            ),
            process.Brick(
                process.Coords3D(1, 1, 5),
                process.Coords3D(1, 1, 6),
            ),
        },
        process.Brick(
            process.Coords3D(0, 1, 4),
            process.Coords3D(2, 1, 4),
        ): {
            process.Brick(
                process.Coords3D(1, 1, 5),
                process.Coords3D(1, 1, 6),
            )
        },
    }

    assert process.sum_chain_reaction_fallen_bricks(chain_reaction_fallen_bricks) == 7


def test_falling_bricks_where_one_brick_has_dependents_that_fall_and_dependents_that_dont_fall():
    brick_input = """\
0,0,1~2,0,1
0,2,1~2,2,1
0,0,2~0,1,2
2,0,2~2,2,2
"""
    bricks = process.parse(brick_input)
    fallen_bricks, fallen_brick_coords = process.falling_bricks(bricks)
    hierarchy = process.brick_dependency_hierarchy(fallen_bricks, fallen_brick_coords)
    assert hierarchy == {
        process.Brick(
            process.Coords3D(0, 0, 1),
            process.Coords3D(2, 0, 1),
        ): {
            process.Brick(
                process.Coords3D(0, 0, 2),
                process.Coords3D(0, 1, 2),
            ),
            process.Brick(process.Coords3D(2, 0, 2), process.Coords3D(2, 2, 2)),
        },
        process.Brick(
            process.Coords3D(0, 2, 1),
            process.Coords3D(2, 2, 1),
        ): {process.Brick(process.Coords3D(2, 0, 2), process.Coords3D(2, 2, 2))},
        process.Brick(
            process.Coords3D(0, 0, 2),
            process.Coords3D(0, 1, 2),
        ): set(),
        process.Brick(process.Coords3D(2, 0, 2), process.Coords3D(2, 2, 2)): set(),
    }
    dependent_count = process.calculate_dependent_count(hierarchy)
    disintegrable, _ = process.disintegrable_bricks(hierarchy, dependent_count)
    assert disintegrable == [
        process.Brick(
            process.Coords3D(0, 2, 1),
            process.Coords3D(2, 2, 1),
        ),
        process.Brick(
            process.Coords3D(0, 0, 2),
            process.Coords3D(0, 1, 2),
        ),
        process.Brick(process.Coords3D(2, 0, 2), process.Coords3D(2, 2, 2)),
    ]
    assert len(disintegrable) == 3
