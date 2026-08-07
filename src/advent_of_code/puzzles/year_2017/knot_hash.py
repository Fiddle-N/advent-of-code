from collections import deque
from itertools import batched
from operator import xor
from functools import reduce

from advent_of_code.common import int_to_hex, int_to_binary

STANDARD_MARKS = 256
SPARSE_HASH_ROUNDS = 64
SPARSE_HASH_BLOCKS = 16
EXTRA_KNOT_HASH_LENGTHS = [17, 31, 73, 47, 23]


class KnotHashResult:
    def __init__(self, result: list[int]):
        self.result = result

    def bindigest(self):
        return "".join(int_to_binary(hash_val, padding=8) for hash_val in self.result)

    def hexdigest(self):
        return "".join(int_to_hex(hash_val, padding=2) for hash_val in self.result)


def run_knot_hash_round(
    lengths: list[int], marks: int = STANDARD_MARKS, rounds: int = 1
) -> list[int]:
    string_circle = deque(range(marks))
    buffer = []
    rotations = 0
    skip = 0

    for _ in range(rounds):
        for length in lengths:
            for _ in range(length):
                buffer.append(string_circle.popleft())
            string_circle.extendleft(buffer)  # reverses elements in buffer
            buffer.clear()

            rotate_val = length + skip
            rotations += rotate_val
            rotations %= marks
            string_circle.rotate(-(rotate_val))

            skip += 1

    string_circle.rotate(rotations)
    return list(string_circle)


def _calculate_sparse_hash(lengths: list[int]) -> list[int]:
    lengths = lengths.copy()
    lengths.extend(EXTRA_KNOT_HASH_LENGTHS)
    return run_knot_hash_round(lengths, marks=STANDARD_MARKS, rounds=SPARSE_HASH_ROUNDS)


def _calculate_dense_hash(lengths: list[int]) -> list[int]:
    return [reduce(xor, block) for block in batched(lengths, SPARSE_HASH_BLOCKS)]


def calculate_knot_hash(input_: str) -> KnotHashResult:
    ascii_vals = [ord(char) for char in input_]
    sparse_hash = _calculate_sparse_hash(ascii_vals)
    dense_hash = _calculate_dense_hash(sparse_hash)
    return KnotHashResult(dense_hash)
