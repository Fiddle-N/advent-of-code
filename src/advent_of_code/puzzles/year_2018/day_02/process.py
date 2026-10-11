from collections import Counter
from collections.abc import Sequence
from itertools import combinations

from advent_of_code.common import read_file, timed_run


def calculate_checksum(ids: Sequence[str]) -> int:
    twos_count = 0
    threes_count = 0
    for id_ in ids:
        letter_counts = Counter(id_).values()
        if 2 in letter_counts:
            twos_count += 1
        if 3 in letter_counts:
            threes_count += 1
    return twos_count * threes_count


def get_correct_ids_common_letters(ids: Sequence[str]) -> str:
    for id_1, id_2 in combinations(ids, 2):
        diffs = 0
        for char_idx, (char1, char2) in enumerate(zip(id_1, id_2)):
            if char1 != char2:
                diffs += 1
                diff_idx = char_idx
        if diffs == 1:
            id_1_allege = id_1[:diff_idx] + id_1[diff_idx + 1 :]
            id_2_allege = id_2[:diff_idx] + id_2[diff_idx + 1 :]
            assert id_1_allege == id_2_allege
            return id_2_allege
    raise ValueError("one solution of correct ids must be present")


def run():
    ids = read_file().splitlines()
    print(calculate_checksum(ids))
    print(get_correct_ids_common_letters(ids))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
