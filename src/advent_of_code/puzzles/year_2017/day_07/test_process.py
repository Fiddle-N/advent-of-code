from advent_of_code.puzzles.year_2017.day_07 import process


def test_seek_unbalanced_weight() -> None:
    program_text = """\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""
    pp = process.ProgramParser()
    program = pp.parse(program_text)
    assert program.name == "tknk"

    req_weight = process.seek_unbalanced_weight(program)
    assert req_weight == 60
