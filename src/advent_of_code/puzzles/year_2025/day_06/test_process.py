from advent_of_code.puzzles.year_2025.day_06 import process


def test_math_expr_part_1_calculate():
    exprs = process.parse(
        """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """,
        "part_1",
    )
    assert process.calculate(exprs) == 4277556


def test_math_expr_part_2_calculate():
    exprs = process.parse(
        """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """,
        "part_2",
    )
    assert process.calculate(exprs) == 3263827
