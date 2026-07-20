import hashlib
from itertools import count
from functools import cache

import more_itertools

from advent_of_code.common import (
    timed_run,
    read_file,
)


NO_OF_KEYS = 64
KEY_STRETCHING_ADDITIONAL_HASHES = 2016


class MD5KeySearch:
    def __init__(self, prefix_salt: str, key_stretching: bool = False):
        self.prefix_salt = prefix_salt
        self.key_stretching = key_stretching

    @cache
    def _hash(self, idx: int) -> str:
        val = self.prefix_salt + str(idx)
        repetitions = KEY_STRETCHING_ADDITIONAL_HASHES + 1 if self.key_stretching else 1
        for _ in range(repetitions):
            val = val.encode()
            val = hashlib.md5(val).hexdigest()
        return val

    @cache
    def _check_quintuplet(self, idx: int, char: str) -> bool:
        hash_val = self._hash(idx)
        for window in more_itertools.windowed(hash_val, 5):
            uniq_chars = set(window)
            if len(uniq_chars) == 1 and next(iter(uniq_chars)) == char:
                return True
        return False

    def _check_triplet(self, idx: int) -> str | None:
        hash_val = self._hash(idx)
        for window in more_itertools.windowed(hash_val, 3):
            uniq_chars = set(window)
            if len(uniq_chars) == 1:
                return next(iter(uniq_chars))
        return None

    def search(self) -> int:
        keys_found = 0
        for idx in count():
            triplet_char = self._check_triplet(idx)
            if triplet_char is None:
                continue

            is_key = False
            for quint_idx in range(idx + 1, idx + 1 + 1000):
                is_quintuplet = self._check_quintuplet(quint_idx, triplet_char)
                if is_quintuplet:
                    is_key = True

            if is_key:
                keys_found += 1

            if keys_found == NO_OF_KEYS:
                return idx
        raise Exception("unreachable code")


def run() -> None:
    prefix_salt = read_file()
    md5_ks = MD5KeySearch(prefix_salt)
    print(md5_ks.search())
    md5_ks_ks = MD5KeySearch(prefix_salt, key_stretching=True)
    print(md5_ks_ks.search())


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
