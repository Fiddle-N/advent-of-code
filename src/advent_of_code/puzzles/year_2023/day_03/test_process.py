from advent_of_code.puzzles.year_2023.day_03 import process


def test_parts():
    schematic_text = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    schematic = process.EngineSchematic(schematic_text)
    assert sorted(schematic.parts) == [35, 467, 592, 598, 617, 633, 664, 755]
    assert sum(schematic.parts) == 4361


def test_gear_parts():
    schematic_text = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    schematic = process.EngineSchematic(schematic_text)
    sorted_gear_parts = sorted(
        tuple(sorted(gear_part)) for gear_part in schematic.gear_parts
    )
    assert sorted_gear_parts == [(35, 467), (598, 755)]
    gear_ratios = process.calculate_gear_ratios(sorted_gear_parts)
    assert gear_ratios == [16345, 451490]
    assert sum(gear_ratios) == 467835
