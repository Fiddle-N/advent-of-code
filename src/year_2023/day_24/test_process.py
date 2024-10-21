import pytest

from year_2023.day_24 import process

@pytest.mark.parametrize(
    "a, b, exp_result, exp_x, exp_y",
    [
        (
            
            process.Vec(process.VecCmpnt(19, -2), process.VecCmpnt(13, 1), process.VecCmpnt(30, -2)), 
            process.Vec(process.VecCmpnt(18, -1), process.VecCmpnt(19, -1), process.VecCmpnt(22, -2)), 
            process.PathOutcome.CROSSED_INSIDE_AREA,
            14.3333333,
            15.3333333,
        ),
        (
            
            process.Vec(process.VecCmpnt(19, -2), process.VecCmpnt(13, 1), process.VecCmpnt(30, -2)), 
            process.Vec(process.VecCmpnt(20, -2), process.VecCmpnt(25, -2), process.VecCmpnt(34, -4)), 
            process.PathOutcome.CROSSED_INSIDE_AREA,
            11.6666666,
            16.6666666,
        ),
        (
            
            process.Vec(process.VecCmpnt(19, -2), process.VecCmpnt(13, 1), process.VecCmpnt(30, -2)), 
            process.Vec(process.VecCmpnt(12, -1), process.VecCmpnt(31, -2), process.VecCmpnt(28, -1)), 
            process.PathOutcome.CROSSED_OUTSIDE_AREA,
            6.2,
            19.4,
        ),
        (
            
            process.Vec(process.VecCmpnt(18, -1), process.VecCmpnt(19, -1), process.VecCmpnt(22, -2)), 
            process.Vec(process.VecCmpnt(12, -1), process.VecCmpnt(31, -2), process.VecCmpnt(28, -1)), 
            process.PathOutcome.CROSSED_OUTSIDE_AREA,
            -6,
            -5,
        ),
        (
            
            process.Vec(process.VecCmpnt(20, -2), process.VecCmpnt(25, -2), process.VecCmpnt(34, -4)), 
            process.Vec(process.VecCmpnt(12, -1), process.VecCmpnt(31, -2), process.VecCmpnt(28, -1)), 
            process.PathOutcome.CROSSED_OUTSIDE_AREA,
            -2,
            3,
        ),
    ],
)
def test_calculate_crossing_2d_crossed(
    a, b, exp_result, exp_x, exp_y
):
    result = process.calculate_crossing_2d(a, b, min_=7, max_=27)
    assert result[0] == exp_result
    assert result[1] is not None
    assert result[1].x == pytest.approx(exp_x)
    assert result[1].y == pytest.approx(exp_y)


@pytest.mark.parametrize(
    "a, b, exp_result",
    [
        (
            
            process.Vec(process.VecCmpnt(19, -2), process.VecCmpnt(13, 1), process.VecCmpnt(30, -2)), 
            process.Vec(process.VecCmpnt(20, 1), process.VecCmpnt(19, -5), process.VecCmpnt(15, -3)), 
            process.PathOutcome.CROSSED_IN_PAST_FOR_A,
        ),
        (
            
            process.Vec(process.VecCmpnt(18, -1), process.VecCmpnt(19, -1), process.VecCmpnt(22, -2)), 
            process.Vec(process.VecCmpnt(20, -2), process.VecCmpnt(25, -2), process.VecCmpnt(34, -4)), 
            process.PathOutcome.PARALLEL,
        ),
        (
            
            process.Vec(process.VecCmpnt(18, -1), process.VecCmpnt(19, -1), process.VecCmpnt(22, -2)), 
            process.Vec(process.VecCmpnt(20, 1), process.VecCmpnt(19, -5), process.VecCmpnt(15, -3)),
            process.PathOutcome.CROSSED_IN_PAST_FOR_BOTH,
        ),
        (
            
            process.Vec(process.VecCmpnt(20, -2), process.VecCmpnt(25, -2), process.VecCmpnt(34, -4)), 
            process.Vec(process.VecCmpnt(20, 1), process.VecCmpnt(19, -5), process.VecCmpnt(15, -3)),
            process.PathOutcome.CROSSED_IN_PAST_FOR_B,
        ),
        (
            process.Vec(process.VecCmpnt(12, -1), process.VecCmpnt(31, -2), process.VecCmpnt(28, -1)),
            process.Vec(process.VecCmpnt(20, 1), process.VecCmpnt(19, -5), process.VecCmpnt(15, -3)),
            process.PathOutcome.CROSSED_IN_PAST_FOR_BOTH,
        ),
    ],
)
def test_calculate_crossing_2d_did_not_cross(
    a, b, exp_result
):
    result = process.calculate_crossing_2d(a, b, min_=7, max_=27)
    assert result[0] == exp_result
    assert result[1] is None


def test_sum_intercepting_vecs_2d():
    vec_text = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    vecs = process.parse_vectors(vec_text)
    assert process.sum_intersecting_vecs_2d(vecs, min_=7, max_=27) == 2


