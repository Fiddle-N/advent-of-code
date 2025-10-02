"""
2015 Day 112

Part 1
Parse JSON and sum all the numbers in the structure.

Part 2
Part 1, but ignore any JSON objects with any property with the value "red"
"""

import json
from typing import Any

from advent_of_code.common import read_file, timed_run


class JSONSumNumbers:
    def __init__(self):
        self._sum = 0
        self._ignore_red = False

    def sum_numbers(self, json_str: str, ignore_red: bool = False) -> int:
        self._sum = 0
        self._ignore_red = ignore_red
        decoded = json.loads(json_str)
        self._sum_numbers(decoded)
        return self._sum

    def _sum_numbers(self, decoded: Any) -> None:
        if isinstance(decoded, dict):
            vals = decoded.values()
            if self._ignore_red and "red" in vals:
                return
        else:
            vals = decoded

        for val in vals:
            match val:
                case int():
                    self._sum += val
                case list() | dict():
                    self._sum_numbers(val)


def run():
    json_str = read_file()
    jsn = JSONSumNumbers()
    print(jsn.sum_numbers(json_str))
    print(jsn.sum_numbers(json_str, ignore_red=True))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
