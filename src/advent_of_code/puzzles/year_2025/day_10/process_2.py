from dataclasses import dataclass

import pulp

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


def calculate_max_presses(machine: Machine) -> list[int]:
    # the smallest joltage target per each joltage that a button affects
    # is that button's max number of times it can be pressed
    # for pressing it more times leads to overflowing the target
    return [min(machine.joltages[idx] for idx in button) for button in machine.buttons]


def solve_int_lin_prob(machine: Machine) -> int:
    # Create problem
    prob = pulp.LpProblem("ButtonPresses", pulp.LpMinimize)

    # Variables
    x = [
        pulp.LpVariable(f"x{idx}", lowBound=0, cat="Integer")
        for idx, _ in enumerate(machine.buttons)
    ]

    # Objective
    prob += pulp.lpSum(x)

    # Constraints
    for target_idx, target_val in enumerate(machine.joltages):
        prob += (
            pulp.lpSum(
                x[touches_idx]
                for touches_idx, touches_val in enumerate(machine.buttons)
                if target_idx in touches_val
            )
            == target_val
        )

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Print solution
    return int(pulp.value(prob.objective))


def run():
    machines = parse(read_file())
    print(sum(solve_int_lin_prob(machine) for machine in machines))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
