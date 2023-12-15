import dataclasses
import enum


ASH = '.'
ROCKS = '#'

TERRAIN_OPPOSITE = {
    ASH: ROCKS,
    ROCKS: ASH,
}


class Orientation(enum.Enum):
    HORIZONTAL = enum.auto()
    VERTICAL = enum.auto()


@dataclasses.dataclass(frozen=True)
class Mirror:
    orientation: Orientation
    position: int


class Patterns:

    def __init__(self, pattern_input):
        self.patterns = pattern_input.split('\n\n')

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())

    def find_mirrors(self):
        clean_mirrors = []
        for pattern in self.patterns:
            clean_mirrors_for_pattern = self._analyse_pattern([pattern], first_mirror=True)
            if clean_mirrors_for_pattern is None:
                raise ValueError('mirror not found')
            clean_mirror, = clean_mirrors_for_pattern
            clean_mirrors.append(clean_mirror)

        dirty_mirrors = []
        for clean_mirror, pattern in zip(clean_mirrors, self.patterns):
            pattern_instances = self._get_instances(pattern)
            dirty_mirrors_for_pattern = self._analyse_pattern(pattern_instances, first_mirror=False)
            assert len(dirty_mirrors_for_pattern) in (1, 2)
            dirty_mirrors_for_pattern.remove(clean_mirror)
            assert len(dirty_mirrors_for_pattern) == 1
            dirty_mirror, = dirty_mirrors_for_pattern
            dirty_mirrors.append(dirty_mirror)

        return clean_mirrors, dirty_mirrors

    def _get_instances(self, pattern):
        instances = []
        left_pattern = []
        right_pattern = list(pattern)
        while right_pattern:
            char = right_pattern.pop(0)
            opposite_char = TERRAIN_OPPOSITE.get(char, char)    # return newline if newline present
            instance = ''.join(left_pattern) + opposite_char + ''.join(right_pattern)
            left_pattern.append(char)
            instances.append(instance)
        return instances

    def _analyse_pattern(self, pattern_instances, first_mirror=True):
        mirrors = set()
        for pattern_instance in pattern_instances:
            pattern_rows = pattern_instance.splitlines()
            row_mirrors = self._analyse_pattern_instance(pattern_rows, first_mirror)
            if row_mirrors:
                for row_mirror in row_mirrors:
                    mirrors.add(Mirror(orientation=Orientation.HORIZONTAL, position=row_mirror))
                if first_mirror:
                    return mirrors
            pattern_cols = list(list(col) for col in zip(*pattern_rows))
            col_mirrors = self._analyse_pattern_instance(pattern_cols, first_mirror)
            if col_mirrors:
                for col_mirror in col_mirrors:
                    mirrors.add(Mirror(orientation=Orientation.VERTICAL, position=col_mirror))
                if first_mirror:
                    return mirrors
        return mirrors

    def _analyse_pattern_instance(self, pattern_rows, first_mirror):
        mirrors = []
        left_rows = []
        right_rows = pattern_rows.copy()
        while True:
            left_rows.append(right_rows.pop(0))     # potentially slow
            if not right_rows:
                break
            reflected_row_no = min(len(left_rows), len(right_rows))
            if left_rows[-reflected_row_no:] == list(reversed(right_rows[:reflected_row_no])):
                mirrors.append(len(left_rows))
                if first_mirror:
                    return mirrors
        return mirrors


def summarise(mirrors):
    factor = {
        Orientation.HORIZONTAL: 100,
        Orientation.VERTICAL: 1,
    }
    return sum(
        factor[mirror.orientation] * mirror.position
        for mirror in mirrors
    )


def main() -> None:
    patterns = Patterns.read_file()
    clean_mirrors, dirty_mirrors = patterns.find_mirrors()
    print(
        "Summary of patterns:",
        summarise(clean_mirrors)
    )
    print(
        "Summary of patterns for dirty mirrors:",
        summarise(dirty_mirrors)
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
