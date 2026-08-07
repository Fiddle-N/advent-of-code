from advent_of_code.puzzles.year_2017.day_13 import process


def test_simulate_firewall():
    raw_firewall = """\
0: 3
1: 2
4: 4
6: 4"""
    firewall = process.parse_firewall(raw_firewall)
    assert process.simulate_firewall(firewall) == (24, 10)
