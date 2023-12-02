from dataclasses import dataclass
from typing import Self, Collection

import parse


@dataclass(frozen=True)
class CubeSelection:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __le__(self, other: Self) -> bool:
        return (
            self.red <= other.red
            and self.green <= other.green
            and self.blue <= other.blue
        )

    @property
    def power(self) -> int:
        return self.red * self.green * self.blue


ELF_QUESTION_CUBE_SELECTION = CubeSelection(red=12, green=13, blue=14)


def read_file() -> str:
    with open("input.txt") as f:
        return f.read()


def generate_games_record(record_str: str) -> dict[int, list[CubeSelection]]:
    record = {}
    for game in record_str.splitlines():
        label, game_info = game.split(': ')
        id_ = parse.parse('Game {id:d}', label)['id']
        record_entry = []
        for set_info in game_info.split('; '):
            cube_selection = {}
            for colour_set_ in set_info.split(', '):
                no, colour = colour_set_.split()
                no = int(no)
                cube_selection[colour] = no
            record_entry.append(CubeSelection(**cube_selection))
        record[id_] = record_entry
    return record


def calculate_min_no_of_cubes_needed(record) -> dict[int, CubeSelection]:
    possible_games = {}
    for id_, record_entry in record.items():
        cubes_needed_for_game = {}
        for colour in ['red', 'green', 'blue']:
            cubes_needed_for_colour = getattr(
                max(
                    record_entry,
                    key=lambda cube_selection: getattr(cube_selection, colour)
                ),
                colour
            )
            cubes_needed_for_game[colour] = cubes_needed_for_colour
        possible_games[id_] = CubeSelection(**cubes_needed_for_game)
    return possible_games


def games_possible_with(
        min_no_of_cubes_needed: dict[int, CubeSelection],
        possible_cube_selection: CubeSelection
) -> list[int]:
    possible_games = []
    for id_, max_cube_selection in min_no_of_cubes_needed.items():
        if max_cube_selection <= possible_cube_selection:
            possible_games.append(id_)
    return possible_games


def generate_power_levels(cube_sets: Collection[CubeSelection]) -> list[int]:
    return [cube_set.power for cube_set in cube_sets]


def main() -> None:
    games_record = generate_games_record(read_file())
    min_number_of_cubes_needed = calculate_min_no_of_cubes_needed(games_record)
    print(
        f"Sum of game IDs possible if bag loaded with {ELF_QUESTION_CUBE_SELECTION}:",
        sum(games_possible_with(min_number_of_cubes_needed, ELF_QUESTION_CUBE_SELECTION)),
    )
    min_number_of_cubes_power_level = generate_power_levels(min_number_of_cubes_needed.values())
    print(
        f"Sum of power of minimum sets of cubes present:",
        sum(min_number_of_cubes_power_level),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
