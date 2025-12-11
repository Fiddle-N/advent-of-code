import collections
from dataclasses import dataclass

from advent_of_code.common import read_file, timed_run

ON = "#"


@dataclass
class Machine:
    lights: int
    buttons: list[int]


@dataclass(frozen=True)
class LightState:
    lights: int
    pressed: int
    visited: int


def parse(raw_input: str) -> list[Machine]:
    lines = raw_input.splitlines()
    machines = []
    for line in lines:
        sections = line.split()

        raw_lights = sections[0]
        raw_buttons = sections[1:-1]

        lights_bin = "".join(str(int(light == ON)) for light in raw_lights[1:-1])
        num_lights = len(lights_bin)
        lights = int(lights_bin, base=2)

        buttons = []
        for raw_button in raw_buttons:
            idxs = [int(ind) for ind in raw_button[1:-1].split(",")]
            button_bin = "".join(str(int(ind in idxs)) for ind in range(num_lights))
            buttons.append(int(button_bin, base=2))

        machines.append(Machine(lights, buttons))
    return machines


def bit_set(bit: int):
    return 1 << bit


def bfs(machine: Machine) -> int:
    if machine.lights == 0:
        return 0

    q = collections.deque()
    q.append(
        LightState(lights=machine.lights, pressed=0, visited=bit_set(machine.lights))
    )
    while True:
        state = q.popleft()
        for button in machine.buttons:
            next_lights = state.lights ^ button
            next_pressed = state.pressed + 1
            if next_lights == 0:
                return next_pressed
            if state.visited & bit_set(next_lights):
                # already visited
                continue
            next_visited = state.visited | bit_set(next_lights)
            q.append(
                LightState(
                    lights=next_lights, pressed=next_pressed, visited=next_visited
                )
            )


def run():
    machines = parse(read_file())
    print(sum(bfs(machine) for machine in machines))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
