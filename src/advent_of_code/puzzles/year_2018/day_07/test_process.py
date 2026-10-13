from advent_of_code.puzzles.year_2018.day_07 import process


def test_assemble_sleigh_1_worker():
    raw_dependencies = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""
    dependencies = process.parse_dependencies(raw_dependencies)
    step_order, _ = process.assemble_sleigh(
        dependencies, n_workers=1, step_time_constant=0
    )
    assert step_order == "CABDFE"


def test_assemble_sleigh_multiple_workers():
    raw_dependencies = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""
    dependencies = process.parse_dependencies(raw_dependencies)
    assert process.assemble_sleigh(dependencies, n_workers=2, step_time_constant=0) == (
        "CABFDE",
        15,
    )
