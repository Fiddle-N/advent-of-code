from advent_of_code.puzzles.year_2017.day_18 import process


def test_run_singlet() -> None:
    raw_instrs = """\
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""
    instrs = process.parse(raw_instrs)
    assert process.run_singlet(instrs=instrs) == 4


def test_run_duet() -> None:
    raw_instrs = """\
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""
    instrs = process.parse(raw_instrs)
    assert process.run_duet(instrs=instrs) == 3
