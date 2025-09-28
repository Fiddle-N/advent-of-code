"""
2015 Day 8

Part 1
Calculate the length of characters of code for given string literals, minus the number of characters in memory for each
one. String literals have double quotes and escape sequences of \\, \" and \xab for a hex character.

Part 2
Encode the code representation of given string literals as a new string, then repeat the same analysis in Part 1.
"""

import ast
import json
from collections.abc import Sequence

from advent_of_code.common import read_file, timed_run


def process_text(lines: Sequence[str]) -> int:
    return sum(len(line) - len(ast.literal_eval(line)) for line in lines)


def encode(lines: Sequence[str]) -> list[str]:
    return [json.dumps(line) for line in lines]


def run() -> None:
    text = read_file()
    lines = text.splitlines()
    print(process_text(lines))

    encoded_lines = encode(lines)
    print(process_text(encoded_lines))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
