"""
2015 Day 4

Part 1
Given a secret key and a number appended to it, find the lowest appended number to create a hex digest beginning with
5 zeroes.

Part 2
Repeat with 6 zeroes.
"""

import hashlib
from advent_of_code.common import read_file


def md5_search(secret_key: str, prefix="00000") -> int:
    secret_bytes = secret_key.encode()
    num = 0
    while True:
        num += 1
        hash_input = secret_bytes + str(num).encode()
        hash_hex = hashlib.md5(hash_input).hexdigest()
        if hash_hex.startswith(prefix):
            return num


def main() -> None:
    secret_key = read_file()
    print(md5_search(secret_key, prefix="00000"))
    print(md5_search(secret_key, prefix="000000"))


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
