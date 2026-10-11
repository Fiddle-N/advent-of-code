from itertools import cycle, accumulate

from advent_of_code.common import read_file, timed_run, parse_ints


def calculate_total_freq(freqs: list[int]) -> int:
    return sum(freqs)


def calculate_first_freq_reached_twice(freqs: list[int]) -> int:
    iter_freqs = accumulate(cycle(freqs))
    seen_freqs = {0}  # add zero in to include starting freq
    for freq in iter_freqs:
        if freq in seen_freqs:
            return freq
        seen_freqs.add(freq)
    raise ValueError("freqs cannot be empty")


def run():
    raw_freqs = read_file()
    freqs = parse_ints(raw_freqs)
    print(calculate_total_freq(freqs))
    print(calculate_first_freq_reached_twice(freqs))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
