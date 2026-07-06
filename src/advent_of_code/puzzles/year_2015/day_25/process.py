import re

from advent_of_code.common import read_file, timed_run

START = 20151125
MUL_OPERAND = 252533
MOD_OPERAND = 33554393


def parse_machine_msg(raw_msg: str) -> tuple[int, int]:
    if (
        matched_msg := re.fullmatch(
            r"To continue, please consult the code grid in the manual.  "
            r"Enter the code at row (?P<row>\d+), column (?P<col>\d+).",
            raw_msg,
        )
    ) is not None:
        return int(matched_msg.group("row")), int(matched_msg.group("col"))
    raise ValueError


def write_codes(row_end: int, col_end: int) -> dict[tuple[int, int], int]:
    codes = {}
    code = None
    total = 2
    while True:
        for col in range(1, total):
            row = total - col
            code = START if code is None else (code * MUL_OPERAND) % MOD_OPERAND
            codes[(row, col)] = code
            if row == row_end and col == col_end:
                return codes
        total += 1


def run():
    raw_msg = read_file()
    row, col = parse_machine_msg(raw_msg)
    codes = write_codes(row_end=row, col_end=col)
    print(codes[(row, col)])


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
