from advent_of_code.puzzles.year_2025.day_05 import process


def test_fresh_ingredient_solver_find_fresh():
    fis = process.FreshIngredientSolver.from_text("""\
3-5
10-14
16-20
12-18

1
5
8
11
17
32""")
    assert fis.find_fresh() == 3


def test_fresh_ingredient_solver_total_fresh():
    fis = process.FreshIngredientSolver.from_text("""\
3-5
10-14
16-20
12-18

1
5
8
11
17
32""")
    assert fis.total_fresh() == 14
