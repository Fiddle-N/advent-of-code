import re
import collections
import copy
import string
import dataclasses
from itertools import count

from advent_of_code.common import read_file, timed_run

DEP_PATTERN = (
    r"Step (?P<dependency>\w) must be finished before step (?P<dependent>\w) can begin."
)


def parse_dependencies(raw_dependencies: str) -> dict[str, list[str]]:
    deps = collections.defaultdict(list)
    for raw_dep in raw_dependencies.splitlines():
        dep_match = re.fullmatch(DEP_PATTERN, raw_dep)
        assert dep_match is not None
        deps[dep_match["dependency"]]  # initialise letters that have no dependencies
        deps[dep_match["dependent"]].append(dep_match["dependency"])
    return dict(deps)


@dataclasses.dataclass
class Worker:
    number: int
    _seconds_remaining: int = 0
    step: str | None = None

    @property
    def seconds_remaining(self) -> int:
        return self._seconds_remaining

    @seconds_remaining.setter
    def seconds_remaining(self, value) -> None:
        if value < 0:
            value = 0
        self._seconds_remaining = value


class _SleighAssembler:
    def __init__(
        self,
        dependencies: dict[str, list[str]],
        n_workers: int,
        step_time_constant: int,
    ):
        self.dependencies = copy.deepcopy(dependencies)
        self.steps = sorted(list(dependencies))
        self.remaining_steps = self.steps.copy()
        self.done = []
        self.workers = [Worker(worker_no) for worker_no in range(n_workers)]
        self.step_time_constant = step_time_constant

    def _remove_dependency(self, step: str) -> None:
        for step_dependency in self.dependencies.values():
            if step in step_dependency:
                step_dependency.remove(step)

    def _finalise_step(self, worker: Worker) -> None:
        if worker.step is not None:
            self._remove_dependency(worker.step)
            self.done.append(worker.step)
            worker.step = None

    def _assign_step(self, worker: Worker) -> None:
        for step in self.remaining_steps.copy():
            if self.dependencies[step]:
                continue

            # letter has no dependencies - assign
            time = self.step_time_constant + string.ascii_uppercase.index(step) + 1
            worker.seconds_remaining = time
            worker.step = step

            self.remaining_steps.remove(step)
            break

    def assemble(self) -> tuple[str, int]:
        for seconds in count():
            for worker in self.workers:
                if worker.seconds_remaining == 0:
                    self._finalise_step(worker)
                    self._assign_step(worker)
                worker.seconds_remaining -= 1
            if set(self.done) == set(self.steps):
                return "".join(self.done), seconds
        raise Exception("unreachable code")


def assemble_sleigh(
    dependencies: dict[str, list[str]], n_workers: int, step_time_constant: int
) -> tuple[str, int]:
    return _SleighAssembler(dependencies, n_workers, step_time_constant).assemble()


def run() -> None:
    raw_dependencies = read_file()
    dependencies = parse_dependencies(raw_dependencies)
    print(assemble_sleigh(dependencies, n_workers=1, step_time_constant=0)[0])
    print(assemble_sleigh(dependencies, n_workers=5, step_time_constant=60)[1])


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
