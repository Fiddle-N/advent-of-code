import dataclasses
import enum
import itertools
import math

import parse

START_ELEMENT = "AAA"
END_ELEMENT = "ZZZ"
START_NODES_LETTER = "A"
END_NODES_LETTER = "Z"


class Direction(enum.Enum):
    LEFT = "L"
    RIGHT = "R"


@dataclasses.dataclass(frozen=True)
class Node:
    left: str
    right: str


class Navigation:
    def __init__(self, nav_input):
        instrs, network = nav_input.split("\n\n")
        self.instrs = [Direction(dir_) for dir_ in instrs]
        self.network = {}
        for node in network.splitlines():
            parsed_node = parse.parse("{input_ele} = ({left_ele}, {right_ele})", node)
            self.network[parsed_node["input_ele"]] = Node(
                parsed_node["left_ele"], parsed_node["right_ele"]
            )

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())


def navigate(nav: Navigation, ele=START_ELEMENT, end=True):
    instr_map = {Direction.LEFT: "left", Direction.RIGHT: "right"}
    for step_no, instr in enumerate(itertools.cycle(nav.instrs), start=1):
        node = nav.network[ele]
        ele = getattr(node, instr_map[instr])
        yield ele
        if end and ele == END_ELEMENT:
            return step_no


def navigate_simultaneously(nav):
    """
    Navigate simultaneously only where paths follow a loop with no offset
    and only one end element is visited in the whole loop
    """
    start_eles = [ele for ele in nav.network if ele.endswith(START_NODES_LETTER)]
    end_ele_steps = []
    for start_ele in start_eles:
        nav_iter = navigate(nav, ele=start_ele, end=False)
        end_nodes = []
        for step in itertools.count(1):
            next_ele = next(nav_iter)
            if next_ele.endswith(END_NODES_LETTER):
                end_nodes.append((next_ele, step))
            if len(end_nodes) == 2:
                break
        end_node_1, end_node_2 = end_nodes
        if end_node_1[0] != end_node_2[0]:
            raise ValueError("More than one end element visited")
        if divmod(end_node_2[1], end_node_1[1]) != (2, 0):
            raise ValueError(
                "Path to end element does not follow a loop with zero offset"
            )
        end_ele_steps.append(end_node_1[1])
    return math.lcm(*end_ele_steps)


def main() -> None:
    nav = Navigation.read_file()
    nav_iter = navigate(nav)
    while True:
        try:
            next(nav_iter)
        except StopIteration as exc:
            steps = exc.value
            break
    print(
        f"Total number of steps required to reach {END_ELEMENT}:",
        steps,
    )
    print(
        f"Total number of steps required to end on a {END_NODES_LETTER} element "
        f"starting from a {START_NODES_LETTER} element simultaneously:",
        navigate_simultaneously(nav),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
