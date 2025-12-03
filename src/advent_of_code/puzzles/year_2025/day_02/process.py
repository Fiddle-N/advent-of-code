from dataclasses import dataclass

from advent_of_code.common import read_file, timed_run


@dataclass(frozen=True)
class IDRange:
    start: int
    end: int


def parse(raw_input: str) -> list[IDRange]:
    id_ranges = []
    for raw_range in raw_input.split(","):
        start, end = raw_range.split("-")
        id_ranges.append(IDRange(int(start), int(end)))
    return id_ranges


def check_id_range_two_repetitions(id_ranges: list[IDRange]) -> int:
    invalid_ids = 0
    for id_range in id_ranges:
        # get first seq base
        start_str = str(id_range.start)
        start_len = len(start_str)
        halfway = start_len // 2

        seq_base = int(start_str[:halfway]) if halfway > 0 else id_range.start

        while True:
            seq_base_str = str(seq_base)
            seq = int(seq_base_str + seq_base_str)
            if seq > id_range.end:
                break
            if seq < id_range.start:
                seq_base += 1
                continue
            invalid_ids += seq
            seq_base += 1
    return invalid_ids


def check_id_range_any_repetitions(id_ranges: list[IDRange]) -> int:
    invalid_ids = set()
    for id_range in id_ranges:
        end_str = str(id_range.end)
        end_len = len(end_str)
        pattern_end = (end_len // 2) + 1

        base = 1
        while True:
            repetitions = 2
            while True:
                seq = int(str(base) * repetitions)
                if seq > id_range.end:
                    break
                if seq < id_range.start:
                    repetitions += 1
                    continue

                invalid_ids.add(seq)
                repetitions += 1
            base += 1
            if len(str(base)) > pattern_end:
                break

    return sum(invalid_ids)


def run():
    id_ranges = parse(read_file())
    print(check_id_range_two_repetitions(id_ranges))
    print(check_id_range_any_repetitions(id_ranges))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
