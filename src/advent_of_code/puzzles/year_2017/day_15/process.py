import re
from collections.abc import Iterator

from advent_of_code.common import ones_mask, read_file, timed_run

START_PATTERN = r"Generator (?:A|B) starts with (?P<gen_start>\d+)"

DIVISOR = 2147483647
A_FACTOR = 16807
B_FACTOR = 48271
A_IS_MULTIPLE_OF = 4
B_IS_MULTIPLE_OF = 8
LOW_BITS = 16
COMPARISONS_1 = 40_000_000
COMPARISONS_2 = 5_000_000


def parse_gen_starts(raw_starts: str) -> tuple[int, int]:
    starts = []
    for raw_start in raw_starts.splitlines():
        match = re.fullmatch(START_PATTERN, raw_start)
        assert match
        starts.append(int(match["gen_start"]))
    assert len(starts) == 2
    return (starts[0], starts[1])


def _seq_gen(start: int, factor: int, if_multiple_of: int = 1) -> Iterator[int]:
    curr = start
    while True:
        curr = (curr * factor) % DIVISOR
        if curr % if_multiple_of == 0:
            yield curr


def _judge(a_gen: Iterator[int], b_gen: Iterator[int], comparisons: int) -> int:
    mask = ones_mask(LOW_BITS)
    return sum(
        (a & mask) == (b & mask) for _, a, b in zip(range(comparisons), a_gen, b_gen)
    )


def judge_part_1(a_start: int, b_start: int) -> int:
    a_gen = _seq_gen(a_start, A_FACTOR)
    b_gen = _seq_gen(b_start, B_FACTOR)
    return _judge(a_gen, b_gen, COMPARISONS_1)


def judge_part_2(a_start: int, b_start: int) -> int:
    a_gen = _seq_gen(a_start, A_FACTOR, if_multiple_of=A_IS_MULTIPLE_OF)
    b_gen = _seq_gen(b_start, B_FACTOR, if_multiple_of=B_IS_MULTIPLE_OF)
    return _judge(a_gen, b_gen, COMPARISONS_2)


def run():
    raw_starts = read_file()
    a_start, b_start = parse_gen_starts(raw_starts)
    print(judge_part_1(a_start, b_start))
    print(judge_part_2(a_start, b_start))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
