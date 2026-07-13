import re
from string import ascii_lowercase
from collections import Counter
from dataclasses import dataclass

from advent_of_code.common import (
    read_file,
    timed_run,
)


ROOM_PATTERN = (
    r"(?P<enc_name>[\w-]+)-"
    r"(?P<sector_id>\d+)"
    r"\[(?P<checksum>\w+)\]"
)

NORTH_POLE_ROOM = "northpole object storage"


@dataclass(frozen=True)
class Room:
    enc_name: str
    sector_id: int
    checksum: str

    @property
    def name(self) -> str:
        return "".join(
            " "
            if letter == "-"
            else ascii_lowercase[
                (ascii_lowercase.index(letter) + self.sector_id) % len(ascii_lowercase)
            ]
            for letter in self.enc_name
        )


def parse_room(raw_room: str) -> Room:
    match_ = re.fullmatch(ROOM_PATTERN, raw_room)
    assert match_ is not None
    return Room(
        match_.group("enc_name"),
        int(match_.group("sector_id")),
        match_.group("checksum"),
    )


def parse_rooms(raw_rooms: str) -> list[Room]:
    rooms = []
    for raw_room in raw_rooms.splitlines():
        rooms.append(parse_room(raw_room))
    return rooms


def is_real_room(room: Room) -> bool:
    enc_name_letters = [letter for letter in room.enc_name if letter != "-"]
    letter_count = Counter(enc_name_letters)
    sorted_letters = sorted(letter_count.items(), key=lambda pair: (-pair[1], pair[0]))
    five_letters = "".join(pair[0] for pair in sorted_letters[:5])
    return five_letters == room.checksum


def calculate_real_rooms(rooms: list[Room]) -> list[Room]:
    return [room for room in rooms if is_real_room(room)]


def sum_sector_ids(rooms: list[Room]) -> int:
    return sum(room.sector_id for room in rooms)


def locate_north_pole_room(rooms: list[Room]) -> int:
    for room in rooms:
        if room.name == NORTH_POLE_ROOM:
            return room.sector_id
    raise ValueError("North Pole Room not found")


def run():
    raw_rooms = read_file()
    rooms = parse_rooms(raw_rooms)
    real_rooms = calculate_real_rooms(rooms)
    print(sum_sector_ids(real_rooms))
    print(locate_north_pole_room(real_rooms))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
