import pytest

from advent_of_code.puzzles.year_2016.day_04 import process


@pytest.mark.parametrize(
    "raw_room, is_real_room",
    [
        ("aaaaa-bbb-z-y-x-123[abxyz]", True),
        ("a-b-c-d-e-f-g-h-987[abcde]", True),
        ("not-a-real-room-404[oarel]", True),
        ("totally-real-room-200[decoy]", False),
    ],
)
def test_is_real_room(raw_room: str, is_real_room: bool) -> None:
    room = process.parse_room(raw_room)
    assert process.is_real_room(room) == is_real_room


def test_room_decrypted_name() -> None:
    assert process.Room("qzmt-zixmtkozy-ivhz", 343, "").name == "very encrypted name"
