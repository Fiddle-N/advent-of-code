from advent_of_code.puzzles.year_2016.day_16 import process


def test_generate_data_checksum():
    data = process.generate_data(initial_data="10000", target=20)
    assert data == list("10000011110010000111")
    checksum = process.generate_checksum(data)
    assert checksum == "01100"
