from itertools import count

from advent_of_code.common import read_file, timed_run

TOP_LAYER = 0


def parse_firewall(raw_firewall: str) -> dict[int, int]:
    firewall = {}
    for layer in raw_firewall.splitlines():
        depth, range_ = layer.split(": ")
        firewall[int(depth)] = int(range_)
    return firewall


def _simulate_firewall(
    delay: int, firewall: dict[int, int], fail_fast: bool
) -> tuple[bool, int | None]:
    severity = 0
    caught = False
    for depth, range_ in firewall.items():
        normalised_range = range_ * 2 - 2  # simulates back and forth scanner
        scanner_location = depth + delay
        normalised_location = scanner_location % normalised_range
        if normalised_location == TOP_LAYER:
            if fail_fast:
                return True, None
            caught = True
            severity += depth * range_
    return caught, severity


def simulate_firewall(firewall: dict[int, int]) -> tuple[int, int]:
    _, initial_severity = _simulate_firewall(
        delay=0, firewall=firewall, fail_fast=False
    )
    assert initial_severity is not None
    for delay in count(start=1):
        caught, severity = _simulate_firewall(
            delay=delay, firewall=firewall, fail_fast=True
        )
        if not caught:
            return (initial_severity, delay)
    raise Exception("unreachable code")


def run():
    raw_firewall = read_file()
    firewall = parse_firewall(raw_firewall)
    print(simulate_firewall(firewall))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
