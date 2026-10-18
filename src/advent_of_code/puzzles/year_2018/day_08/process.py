import collections
import dataclasses
from typing import Sequence

from advent_of_code.common import read_file, timed_run


@dataclasses.dataclass
class Node:
    children: Sequence[Node]
    metadata: Sequence[int]

    @property
    def metadata_sum(self) -> int:
        return sum([node.metadata_sum for node in self.children]) + sum(self.metadata)

    @property
    def value(self) -> int:
        if self.children:
            values = []
            for metadatum in self.metadata:
                try:
                    values.append(self.children[metadatum - 1].value)
                except IndexError:
                    pass
            return sum(values)
        else:
            return sum(self.metadata)


class TreeParser:
    def __init__(self, data: str):
        self._data = collections.deque([int(no) for no in data.split()])

    def parse(self) -> Node:
        raw_children = self._data.popleft()
        raw_metadata = self._data.popleft()
        children = [self.parse() for _ in range(raw_children)]
        metadata = [self._data.popleft() for _ in range(raw_metadata)]
        return Node(children, metadata)


def run() -> None:
    data = read_file()
    tree_parser = TreeParser(data)
    tree = tree_parser.parse()
    print(tree.metadata_sum)
    print(tree.value)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
