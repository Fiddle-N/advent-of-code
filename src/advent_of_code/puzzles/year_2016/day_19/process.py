from collections import deque

from advent_of_code.common import read_file, timed_run


def simulate_p1(elves: int) -> int:
    circle = deque(range(1, elves + 1))
    while len(circle) > 1:
        circle.rotate(-1)
        circle.popleft()
    return next(iter(circle))


def simulate_p2(elves: int) -> int:
    circle_l = deque(range(1, 1 + elves // 2))
    circle_r = deque(range(1 + elves // 2, elves + 1))
    while (len(circle_l) + len(circle_r)) > 1:
        # permanently remove elf
        circle_r.popleft()

        # rotate thief
        thief = circle_l.popleft()
        circle_r.append(thief)

        # rebalance
        if len(circle_r) > len(circle_l) + 1:
            elf = circle_r.popleft()
            circle_l.append(elf)

    return next(iter(circle_l + circle_r))


def run():
    elves = int(read_file())
    print(simulate_p1(elves))
    print(simulate_p2(elves))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
