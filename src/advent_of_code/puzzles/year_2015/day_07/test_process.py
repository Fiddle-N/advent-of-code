from advent_of_code.puzzles.year_2015.day_07 import process


def test_assembly() -> None:
    circuit_input = """\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""
    circuit = process.assemble_circuit(circuit_input)
    wire_values = {wire: fn() for wire, fn in circuit.items()}
    assert wire_values == {
        "d": 72,
        "e": 507,
        "f": 492,
        "g": 114,
        "h": 65412,
        "i": 65079,
        "x": 123,
        "y": 456,
    }
