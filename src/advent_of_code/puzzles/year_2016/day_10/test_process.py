from advent_of_code.puzzles.year_2016.day_10 import process


def test_run_instrs():
    instrs = process.Instructions.from_raw_instrs("""\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2""")
    bot_id_check, outputs = process.run_instrs(instrs, low_check=2, high_check=5)
    assert bot_id_check == 2
    assert outputs == (5, 2, 3)
