from collections import deque

from advent_of_code.common import read_file, timed_run

SPINLOCK_INSERTIONS_1 = 2017
SPINLOCK_TARGET_1 = SPINLOCK_INSERTIONS_1
SPINLOCK_INSERTIONS_2 = 50_000_000
SPINLOCK_TARGET_2 = 0


def spinlock(forward_steps: int, cycles: int, search_no: int):
    q = deque([0])
    for num in range(1, cycles + 1):
        q.rotate(-(forward_steps % len(q)))
        q.append(num)
    while q[-1] != search_no:
        q.rotate()
    return q[0]


def run():
    forward_steps = int(read_file())
    print(
        spinlock(
            forward_steps, cycles=SPINLOCK_INSERTIONS_1, search_no=SPINLOCK_TARGET_1
        )
    )
    print(
        spinlock(
            forward_steps, cycles=SPINLOCK_INSERTIONS_2, search_no=SPINLOCK_TARGET_2
        )
    )


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
