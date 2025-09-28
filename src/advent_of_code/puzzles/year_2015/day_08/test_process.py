from advent_of_code.puzzles.year_2015.day_08 import process


def test_process_text() -> None:
    text = r'''""
"abc"
"aaa\"aaa"
"\x27"'''
    lines = text.splitlines()
    assert process.process_text(lines) == 12


def test_process_text_after_encoding() -> None:
    text = r'''""
"abc"
"aaa\"aaa"
"\x27"'''
    lines = text.splitlines()
    encoded_lines = process.encode(lines)
    assert process.process_text(encoded_lines) == 19
