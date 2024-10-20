import collections
import dataclasses
import itertools
import re


_LABEL_PATTERN = r"(?P<label>[A-Za-z]+)"
BOX_ADD_PATTERN = rf"{_LABEL_PATTERN}=(?P<focal_length>[1-9])"
BOX_REMOVE_PATTERN = rf"{_LABEL_PATTERN}-"


def hash_(input_):
    val = 0
    for char in input_:
        val += ord(char)
        val *= 17
        val %= 256
    return val


@dataclasses.dataclass
class BoxLens:
    focal_length: int
    prev: str | None
    next_: str | None


@dataclasses.dataclass(frozen=True)
class BoxAdd:
    label: str
    focal_length: int


@dataclasses.dataclass(frozen=True)
class BoxRemove:
    label: str


class Box:
    """
    Singly-linked list modelled as dictionary (hashmap)
    to allow O(1) access to any label
    """

    def __init__(self):
        self.box: dict[str, BoxLens] = {}
        self.first_label = None
        self.last_label = None

    def execute(self, step: BoxAdd | BoxRemove):
        if isinstance(step, BoxAdd):
            self._add(step.label, step.focal_length)
        elif isinstance(step, BoxRemove):
            self._remove(step.label)
        else:
            raise TypeError('Unrecognised step')

    def _add(self, label, focal_length):
        if label in self.box:
            self.box[label].focal_length = focal_length
        else:
            if not self.box:
                self.first_label = label
            if self.last_label is not None:
                current_last_label = self.box[self.last_label]
                current_last_label.next_ = label
            self.box[label] = BoxLens(
                focal_length=focal_length, prev=self.last_label, next_=None
            )
            self.last_label = label

    def _remove(self, label):
        removed_label = self.box.pop(label, None)
        if removed_label is None:
            return

        prev_label = removed_label.prev
        next_label = removed_label.next_
        prev_lens = self.box.get(prev_label)
        next_lens = self.box.get(next_label)

        if prev_lens:
            prev_lens.next_ = (
                next_label if label != self.last_label else None
            )
        if next_lens:
            next_lens.prev = (
                prev_label if label != self.first_label else None
            )

        if label == self.first_label:
            self.first_label = next_label
        if label == self.last_label:
            self.last_label = prev_label


class LensInstall:

    def __init__(self, init_seq):
        self.init_seq = []
        for step in init_seq:
            if match := re.fullmatch(BOX_ADD_PATTERN, step):
                self.init_seq.append(
                    BoxAdd(
                        label=match.group('label'),
                        focal_length=int(match.group('focal_length'))
                    )
                )
            elif match := re.fullmatch(BOX_REMOVE_PATTERN, step):
                self.init_seq.append(
                    BoxRemove(label=match.group('label'))
                )
            else:
                raise ValueError('Unknown step')
        self.boxes = collections.defaultdict(Box)

    def __iter__(self):
        for step in self.init_seq:
            box_no = int(hash_(step.label))
            box = self.boxes[box_no]
            box.execute(step)
            yield self.boxes


def focusing_power(boxes):
    lens_focusing_power = {}
    for box_no, box in boxes.items():
        if not box.box:
            continue
        box_label = box.first_label
        for slot_no in itertools.count(start=1):
            lens = box.box[box_label]
            power = (box_no + 1) * slot_no * lens.focal_length
            lens_focusing_power[box_label] = power
            box_label = lens.next_
            if box_label is None:
                break
    return lens_focusing_power


def read_file():
    with open("input.txt") as f:
        return f.read().strip()


def main() -> None:
    init_seq = read_file().split(',')
    hashed_init_seq = [hash_(step) for step in init_seq]
    print(
        "Hash of each step of initialisation sequence:",
        sum(hashed_init_seq)
    )
    lens_install = LensInstall(init_seq)
    lens_install_iter = iter(lens_install)
    boxes = None
    for boxes in lens_install_iter:
        pass
    lens_focusing_power = focusing_power(boxes)
    print(
        "Focus power of lens configuration after initialisation sequence:",
        sum(lens_focusing_power.values())
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
