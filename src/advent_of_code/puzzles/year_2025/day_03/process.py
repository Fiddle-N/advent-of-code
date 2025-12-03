from advent_of_code.common import read_file, timed_run


def parse(raw_input: str) -> list[list[int]]:
    return [[int(char) for char in line] for line in raw_input.splitlines()]


def find_max_joltage(banks: list[list[int]], digits: int) -> int:
    max_joltage = 0
    for bank in banks:
        max_joltage_seq: list[int] = []
        bank_pairs = list(enumerate(bank))
        start_idx = 0
        for end_idx in range(-(digits - 1), 1):
            bank_seq = (
                bank_pairs[start_idx:]
                if end_idx == 0
                else bank_pairs[start_idx:end_idx]
            )
            max_pos, max_val = max(bank_seq, key=lambda pair: pair[1])
            max_joltage_seq.append(max_val)
            start_idx = max_pos + 1
        max_joltage_bank = int("".join(str(digit) for digit in max_joltage_seq))
        max_joltage += max_joltage_bank
    return max_joltage


def run():
    banks = parse(read_file())
    print(find_max_joltage(banks, digits=2))
    print(find_max_joltage(banks, digits=12))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
