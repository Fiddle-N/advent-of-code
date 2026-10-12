import string

from advent_of_code.common import read_file, timed_run


def _react_polymer(polymer: str) -> str:
    reactions = []
    for unit in polymer:
        if reactions and unit.swapcase() == reactions[-1]:
            reactions.pop()
        else:
            reactions.append(unit)
    return "".join(reactions)


def react_polymer(polymer: str) -> tuple[int, int]:
    reacted_polymer = _react_polymer(polymer)
    reacted_improved_polymers = [
        _react_polymer(reacted_polymer.replace(char, "").replace(char.upper(), ""))
        for char in string.ascii_lowercase
    ]
    return len(reacted_polymer), len(min(reacted_improved_polymers, key=len))


def run() -> None:
    polymer = read_file()
    print(react_polymer(polymer))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
