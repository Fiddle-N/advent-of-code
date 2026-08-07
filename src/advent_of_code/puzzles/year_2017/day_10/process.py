from advent_of_code.common import read_file, timed_run
from advent_of_code.puzzles.year_2017 import knot_hash


def parse_ints(raw: str) -> list[int]:
    return [int(num) for num in raw.split(",")]


def run():
    raw_lengths = read_file()

    lengths = parse_ints(raw_lengths)
    hash_round_result = knot_hash.run_knot_hash_round(lengths)
    print(hash_round_result[0] * hash_round_result[1])

    hash_result = knot_hash.calculate_knot_hash(raw_lengths)
    print(hash_result.hexdigest())


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
