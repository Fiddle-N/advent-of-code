import re
from dataclasses import dataclass
from collections import deque
from enum import StrEnum, auto
from itertools import combinations_with_replacement

from advent_of_code.common import read_file, timed_run, iter_bits, ones_mask

COMPONENT_PATTERN = (
    r"(?P<element>\w+)"
    r"(?:\-compatible)?"
    r" (?P<comp_type>generator|microchip)"
)


NUMBER_OF_FLOORS = 4
ELEVATOR_BIT_WIDTH = 2


class ComponentType(StrEnum):
    GENERATOR = auto()
    MICROCHIP = auto()


@dataclass(frozen=True, order=True)
class Component:
    element: str
    type: ComponentType


def parse_components(raw_components: str) -> dict[int, list[Component]]:
    components = {}
    for floor, raw_component in enumerate(raw_components.splitlines()):
        floor_comps = []
        for match_ in re.finditer(COMPONENT_PATTERN, raw_component):
            floor_comps.append(
                Component(
                    element=match_["element"],
                    type=ComponentType(match_["comp_type"]),
                )
            )
        components[floor] = floor_comps
    return components


def map_comp_to_floor_no(comps: dict[int, list[Component]]) -> dict[Component, int]:
    comp_to_floor_map = {}
    for floor, floor_comps in comps.items():
        for comp in floor_comps:
            comp_to_floor_map[comp] = floor
    return comp_to_floor_map


def init_floor_mask(
    elements: list[str], comp_to_floor_map: dict[Component, int]
) -> int:
    mask = 0

    # for each floor pack generator bits together then microchip bits together
    for floor in range(NUMBER_OF_FLOORS):
        for ele_type in ComponentType:
            for ele in elements:
                mask <<= 1
                if comp_to_floor_map[Component(ele, ele_type)] == floor:
                    mask |= 1

    # pack 2 bits for the elevator floor
    # we start on floor 0 so this is easy
    mask <<= ELEVATOR_BIT_WIDTH
    return mask


@dataclass(frozen=True)
class ComponentState:
    state: int
    steps: int


class ContainmentSimulator:
    MAX_NO_COMPONENT_TRANSITIONS = 2

    def __init__(self, no_of_elements: int):
        self.no_of_elements = no_of_elements
        self.floor_bit_width = self.no_of_elements * len(ComponentType)

    def _get_floor_bit_offset(self, floor_no) -> int:
        return (
            NUMBER_OF_FLOORS - floor_no - 1
        ) * self.floor_bit_width + ELEVATOR_BIT_WIDTH

    def _get_floor_bits(self, state: int, floor_no: int) -> int:
        # capture bits relating to a particular floor
        return (state >> self._get_floor_bit_offset(floor_no)) & ones_mask(
            self.floor_bit_width
        )

    def _get_comp_bits(self, floor: int) -> tuple[int, int]:
        # split floor bits into generator and microchip bits
        return (
            floor >> self.no_of_elements,
            floor & ones_mask(self.no_of_elements),
        )

    def _set_floor_bits(self, state: int, floor: int, floor_no: int) -> int:
        floor_bit_offset = self._get_floor_bit_offset(floor_no)
        blank_mask = ones_mask(self.floor_bit_width) << floor_bit_offset
        replace_mask = floor << floor_bit_offset
        return (state & ~blank_mask) | replace_mask

    def _set_elevator_bits(
        self,
        state,
        elevator,
    ):
        cleared_elevator_bits = (state >> ELEVATOR_BIT_WIDTH) << ELEVATOR_BIT_WIDTH
        return cleared_elevator_bits | elevator

    def _validate_next_floor(self, next_floor: int) -> bool:
        next_floor_gens, next_floor_chips = self._get_comp_bits(next_floor)

        next_floor_unprotected_chips = next_floor_chips & ~next_floor_gens
        next_floor_other_gens = next_floor_gens & ~next_floor_unprotected_chips

        return not (
            next_floor_unprotected_chips and next_floor_other_gens
        )  # can't move without leaving exposed chips

    def _validate_transition(
        self,
        next_comps: int,
        floor: int,
        adj_floor: int,
    ) -> tuple[int, int] | None:
        # remove objects from current floor
        next_floor = floor & ~next_comps
        if not self._validate_next_floor(next_floor):
            return None

        # add objects to adj floor
        next_adj_floor = adj_floor | next_comps
        if not self._validate_next_floor(next_adj_floor):
            return None

        return (next_floor, next_adj_floor)

    def _next_floors(
        self, state: int, floor_no: int, adj_floor_no: int
    ) -> list[tuple[int, int]]:
        floor = self._get_floor_bits(state, floor_no)
        adj_floor = self._get_floor_bits(state, adj_floor_no)
        next_floors = []
        for comp_1, comp_2 in combinations_with_replacement(
            iter_bits(floor), self.MAX_NO_COMPONENT_TRANSITIONS
        ):
            comps = comp_1 | comp_2
            transition = self._validate_transition(
                comps,
                floor,
                adj_floor,
            )
            if transition is None:
                continue
            next_floors.append(transition)

        return next_floors

    def simulate(self, start: int) -> int:
        # bfs

        # all components are on the highest floor (which are at the lowest bits)
        # and the elevator is at the highest floor
        # (so all elevator bits are set since there are exactly four floors
        # represented by two 1 bits)
        win_condition = ones_mask(self.floor_bit_width + ELEVATOR_BIT_WIDTH)

        q = deque([ComponentState(start, 0)])
        states = {start}

        while q:
            cs = q.pop()
            state = cs.state

            if state == win_condition:
                return cs.steps

            floor_no = state & ones_mask(
                ELEVATOR_BIT_WIDTH
            )  # floor bits are the two lowest bits

            # calculate adjacent floors to current floor
            adj_floor_nos = []
            low_floor = floor_no - 1
            if low_floor >= 0:
                adj_floor_nos.append(low_floor)
            high_floor = floor_no + 1
            if high_floor <= NUMBER_OF_FLOORS - 1:
                adj_floor_nos.append(high_floor)

            for adj_floor_no in adj_floor_nos:
                next_floors = self._next_floors(state, floor_no, adj_floor_no)
                for next_current_floor, next_adj_floor in next_floors:
                    # set next state bits
                    next_state = self._set_floor_bits(
                        state, next_current_floor, floor_no
                    )
                    next_state = self._set_floor_bits(
                        next_state, next_adj_floor, adj_floor_no
                    )
                    next_state = self._set_elevator_bits(next_state, adj_floor_no)

                    if next_state in states:
                        continue
                    states.add(next_state)

                    q.appendleft(ComponentState(next_state, cs.steps + 1))

        raise Exception


def simulate(comps: dict[int, list[Component]]):
    elements = sorted(
        set(comp.element for floor_comps in comps.values() for comp in floor_comps)
    )
    comp_to_floor_map = map_comp_to_floor_no(comps)
    init_mask = init_floor_mask(elements, comp_to_floor_map)
    cs = ContainmentSimulator(len(elements))
    return cs.simulate(init_mask)


def run() -> None:
    raw_comps = read_file()
    comps = parse_components(raw_comps)
    print(simulate(comps))

    for comp in [
        Component(element="elerium", type=ComponentType.GENERATOR),
        Component(element="elerium", type=ComponentType.MICROCHIP),
        Component(element="dilithium", type=ComponentType.GENERATOR),
        Component(element="dilithium", type=ComponentType.MICROCHIP),
    ]:
        comps[0].append(comp)
    print(simulate(comps))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
