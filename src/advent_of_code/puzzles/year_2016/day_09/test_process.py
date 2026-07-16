import pytest

from advent_of_code.puzzles.year_2016.day_09 import process


@pytest.mark.parametrize(
    "raw_compressed_text, length",
    [
        ("ADVENT", 6),
        ("A(1x5)BC", 7),
        ("(3x3)XYZ", 9),
        ("A(2x2)BCD(2x2)EFG", 11),
        ("(6x1)(1x3)A", 6),
        ("X(8x2)(3x3)ABCY", 18),
    ],
)
def test_compressed_text_version_1_decompressed_length(
    raw_compressed_text: str, length: int
) -> None:
    parser_v1 = process.CompressedTextParser(version=1)
    compressed_text = parser_v1.parse(raw_compressed_text)
    assert compressed_text.decompressed_length == length


@pytest.mark.parametrize(
    "raw_compressed_text, length",
    [
        ("(3x3)XYZ", 9),
        ("X(8x2)(3x3)ABCY", 20),
        ("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920),
        ("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", 445),
    ],
)
def test_compressed_text_version_2_decompressed_length(
    raw_compressed_text: str, length: int
) -> None:
    parser_v2 = process.CompressedTextParser(version=2)
    compressed_text = parser_v2.parse(raw_compressed_text)
    assert compressed_text.decompressed_length == length
