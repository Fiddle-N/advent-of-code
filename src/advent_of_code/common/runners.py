import timeit
from collections.abc import Callable

__all__ = ["timed_run"]


def timed_run(fn: Callable) -> None:
    print(f"Ran in {timeit.timeit(fn, number=1)} seconds.")
