from advent_of_code.common import read_file, timed_run


def parse_passphrase(raw_pp: str) -> list[str]:
    return raw_pp.split()


def parse_passphrases(raw_pps: str) -> list[list[str]]:
    return [parse_passphrase(raw_pp) for raw_pp in raw_pps.splitlines()]


def is_valid_passphrase(pp: list[str], added_security: bool = False) -> bool:
    transformed_pp = [(tuple(sorted(word)) if added_security else word) for word in pp]
    return len(pp) == len(set(transformed_pp))


def count_valid_passphrases(pps: list[list[str]], added_security: bool = False) -> int:
    return sum(is_valid_passphrase(pp, added_security) for pp in pps)


def run():
    raw_pps = read_file()
    pps = parse_passphrases(raw_pps)
    print(count_valid_passphrases(pps))
    print(count_valid_passphrases(pps, added_security=True))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
