import itertools
import timeit
from collections.abc import Sequence
from typing import cast

import more_itertools


def count_depth(depths, window=None):
    assert len(depths) >= 3
    depths: Sequence[int] = [int(depth) for depth in depths.splitlines()]
    if window is not None:
        new_depths = []
        for w in more_itertools.windowed(depths, n=3):
            w = cast(tuple[int, ...], w)
            new_depths.append(sum(w))
        depths = new_depths
    increasing = sum(
        depth_pair[1] > depth_pair[0] for depth_pair in itertools.pairwise(depths)
    )
    return increasing


def main():
    with open("input.txt") as f:
        depths = f.read()
        print("Increasing depths:", count_depth(depths))
        print("Increasing depths with window 3:", count_depth(depths, window=3))


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
