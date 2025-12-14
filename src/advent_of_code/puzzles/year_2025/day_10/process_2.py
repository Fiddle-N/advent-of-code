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


def calculate_max_presses(machine: Machine) -> list[int]:
    # the smallest joltage target per each joltage that a button affects
    # is that button's max number of times it can be pressed
    # for pressing it more times leads to overflowing the target
    return [min(machine.joltages[idx] for idx in button) for button in machine.buttons]


class JoltageDFSearcher:
    def __init__(self, machine: Machine):
        self._joltages = machine.joltages
        max_presses_per_button = calculate_max_presses(machine)
        self._buttons = sorted(zip(max_presses_per_button, machine.buttons))

        self._min_presses = None

    def _dfs(self, joltages: list[int], presses: list[int]) -> None:
        print(joltages, presses)
        next_total_presses = sum(presses) + 1
        if self._min_presses is not None and next_total_presses >= self._min_presses:
            return None

        for idx, (max_button_press, button) in enumerate(self._buttons):
            next_presses = presses.copy()
            button_presses = next_presses[idx] + 1
            next_presses[idx] = button_presses

            # calculate if button press goes over max press limit for that button
            if button_presses > max_button_press:
                continue

            # calculate joltages after button press
            next_joltages = []
            max_press_overflow = False
            for idx, joltage in enumerate(joltages):
                if idx in button:
                    next_joltage = joltage - 1
                    if next_joltage < 0:
                        # pushing the button has skipped past our target
                        # skip this button and try the next
                        max_press_overflow = True
                        break
                else:
                    next_joltage = joltage
                next_joltages.append(next_joltage)
            if max_press_overflow:
                continue

            if all(joltage == 0 for joltage in next_joltages):
                # win condition
                # not possible for any other button presses in this for loop to beat this
                # so return immediately
                self._min_presses = next_total_presses
                return None

            # not yet at win condition - recurse
            self._dfs(next_joltages, next_presses)

        return None

    def dfs(self) -> int:
        initial_joltages = self._joltages.copy()
        initial_presses = [0] * len(self._buttons)
        self._dfs(initial_joltages, initial_presses)
        return self._min_presses


def run():
    machines = parse(read_file())
    total = 0
    total_machines = len(machines)
    for num, machine in enumerate(machines):
        df_searcher = JoltageDFSearcher(machine)
        result = df_searcher.dfs()
        total += result
        print(f"{num + 1} of {total_machines}")
    print(total)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
