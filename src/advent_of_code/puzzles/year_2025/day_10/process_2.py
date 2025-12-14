import collections
from dataclasses import dataclass

from advent_of_code.common import read_file, timed_run

ON = "#"


@dataclass
class Machine:
    buttons: list[list[int]]
    joltages: list[int]


@dataclass(frozen=True)
class JoltageState:
    joltages: tuple[int, ...]
    pressed: int


def parse(raw_input: str) -> list[Machine]:
    lines = raw_input.splitlines()
    machines = []
    for line in lines:
        sections = line.split()

        raw_buttons = sections[1:-1]
        raw_joltage = sections[-1]

        buttons = [
            [int(val) for val in raw_button[1:-1].split(",")]
            for raw_button in raw_buttons
        ]
        joltage = [int(val) for val in raw_joltage[1:-1].split(",")]

        machines.append(Machine(buttons, joltage))
    return machines


def bfs(machine: Machine) -> int:
    if all(joltage == 0 for joltage in machine.joltages):
        return 0

    q = collections.deque()
    q.append(JoltageState(joltages=tuple(machine.joltages), pressed=0))
    cache = set()
    while True:
        state = q.popleft()
        if state.joltages in cache:
            continue
        else:
            cache.add(state.joltages)
        for button in machine.buttons:
            next_joltages = []
            next_pressed = state.pressed + 1
            overflow = False
            for idx, joltage in enumerate(state.joltages):
                if idx in button:
                    next_joltage = joltage - 1
                    if next_joltage < 0:
                        overflow = True
                        break
                else:
                    next_joltage = joltage
                next_joltages.append(next_joltage)

            if overflow:
                continue

            if all(joltage == 0 for joltage in next_joltages):
                return next_pressed

            q.append(JoltageState(joltages=tuple(next_joltages), pressed=next_pressed))


def run():
    machines = parse(read_file())
    total = 0
    total_machines = len(machines)
    for num, machine in enumerate(machines):
        result = bfs(machine)
        total += result
        print(f"{num + 1} of {total_machines}")
    print(total)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
