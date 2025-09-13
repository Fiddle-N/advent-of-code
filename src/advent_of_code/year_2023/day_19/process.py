import dataclasses
import enum
import math
import operator
from typing import Literal, Self

import parse


START_NAME = "in"

MIN_VALUE = 1
MAX_VALUE = 4000

OPERATORS = {
    ">": operator.gt,
    "<": operator.lt,
}

OPPOSITE_OPS = {
    ">": "<=",
    ">=": "<",
    "<": ">=",
    "<=": ">",
}


class Result(enum.Enum):
    ACCEPTED = "A"
    REJECTED = "R"


@dataclasses.dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int


@dataclasses.dataclass(frozen=True)
class Condition:
    attr: Literal["x", "m", "a", "s"]
    op: Literal["<", "<=", ">", ">="]
    value: int

    def opposite(self) -> Self:
        return type(self)(attr=self.attr, op=OPPOSITE_OPS[self.op], value=self.value)


@dataclasses.dataclass(frozen=True)
class ConditionRule:
    condition: Condition
    if_true: Result | str


@dataclasses.dataclass
class Workflow:
    condition_rules: list[ConditionRule]
    final_rule: Result | str


@dataclasses.dataclass(frozen=True)
class CategoryRange:
    start: int
    end: int


@dataclasses.dataclass
class PartRanges:
    x: CategoryRange = CategoryRange(MIN_VALUE, MAX_VALUE)
    m: CategoryRange = CategoryRange(MIN_VALUE, MAX_VALUE)
    a: CategoryRange = CategoryRange(MIN_VALUE, MAX_VALUE)
    s: CategoryRange = CategoryRange(MIN_VALUE, MAX_VALUE)


def _parse_outcome(outcome_str: str) -> Result | str:
    try:
        outcome = Result(outcome_str)
    except ValueError:
        outcome = outcome_str
    return outcome


def parse_input(input_: str) -> tuple[dict[str, Workflow], list[Part]]:
    workflow_input, part_rating_input = input_.split("\n\n")

    workflows = {}
    for workflow in workflow_input.splitlines():
        parsed_workflow = parse.parse("{name}{{{rules}}}", workflow)
        rules_input = parsed_workflow["rules"]
        rules_list = [rule for rule in rules_input.split(",")]
        *condition_rules_list, final_rule_str = rules_list

        condition_rules = []
        for condition_rule_str in condition_rules_list:
            parsed_condition = parse.parse(
                "{attr}{op}{value:d}:{if_true}", condition_rule_str
            )
            condition_rule = ConditionRule(
                condition=Condition(
                    attr=parsed_condition["attr"],
                    op=parsed_condition["op"],
                    value=parsed_condition["value"],
                ),
                if_true=_parse_outcome(parsed_condition["if_true"]),
            )
            condition_rules.append(condition_rule)

        final_rule = _parse_outcome(final_rule_str)
        workflows[parsed_workflow["name"]] = Workflow(
            condition_rules=condition_rules, final_rule=final_rule
        )

    parts = []
    for part_str in part_rating_input.splitlines():
        parsed_part = parse.parse("{{x={x:d},m={m:d},a={a:d},s={s:d}}", part_str)
        part = Part(
            x=parsed_part["x"],
            m=parsed_part["m"],
            a=parsed_part["a"],
            s=parsed_part["s"],
        )
        parts.append(part)

    return workflows, parts


def _condition_fn(condition: Condition, part: Part) -> bool:
    op_fn = OPERATORS[condition.op]
    return op_fn(getattr(part, condition.attr), condition.value)


def _run_workflow_rules(workflow: Workflow, part: Part) -> Result | str:
    for condition_rule in workflow.condition_rules:
        condition_result = _condition_fn(condition_rule.condition, part)
        if condition_result:
            return condition_rule.if_true
    return workflow.final_rule


def sort_through_parts(workflows: dict[str, Workflow], parts: list[Part]) -> list[Part]:
    sorted_parts = []
    for part in parts:
        name = START_NAME
        while True:
            workflow = workflows[name]
            outcome = _run_workflow_rules(workflow, part)
            if isinstance(outcome, Result):
                break
            name = outcome
        if outcome == Result.ACCEPTED:
            sorted_parts.append(part)
    return sorted_parts


def sum_parts(parts: list[Part]) -> int:
    return sum([(part.x + part.m + part.a + part.s) for part in parts])


class _WalkAcceptedPaths:
    def __init__(self, workflows: dict[str, Workflow]) -> None:
        self.workflows = workflows
        self.accepted_paths = []

    def _process_outcome(self, outcome: Result | str, path: list[Condition]) -> None:
        if isinstance(outcome, Result):
            if outcome == Result.ACCEPTED:
                self.accepted_paths.append(path)
        else:
            self.walk(path, outcome)

    def walk(self, path: list[Condition] | None = None, name: str = START_NAME) -> None:
        if path is None:
            path = []

        workflow = self.workflows[name]

        for condition_rule in workflow.condition_rules:
            condition = condition_rule.condition

            # if true
            true_path = path.copy()
            true_path.append(condition)
            self._process_outcome(outcome=condition_rule.if_true, path=true_path)

            # if false
            opposite_condition = condition.opposite()
            path.append(opposite_condition)

        self._process_outcome(outcome=workflow.final_rule, path=path)


def _walk_accepted_paths(workflows: dict[str, Workflow]) -> list[Condition]:
    walk_path_runner = _WalkAcceptedPaths(workflows)
    walk_path_runner.walk()
    return walk_path_runner.accepted_paths


def _condition_to_range(condition: Condition) -> CategoryRange:
    match condition.op:
        case "<":
            start = MIN_VALUE
            end = condition.value - 1
        case "<=":
            start = MIN_VALUE
            end = condition.value
        case ">":
            start = condition.value + 1
            end = MAX_VALUE
        case ">=":
            start = condition.value
            end = MAX_VALUE
        case _:
            raise ValueError("Unexpected operator")
    return CategoryRange(start, end)


def _combine_ranges(range1: CategoryRange, range2: CategoryRange) -> CategoryRange:
    is_overlap = (range1.start <= range2.end) and (range2.start <= range1.end)
    if not is_overlap:
        raise Exception("Ranges don't overlap - this path is invalid")
    overlap_start = max(range1.start, range2.start)
    overlap_end = min(range1.end, range2.end)
    return CategoryRange(start=overlap_start, end=overlap_end)


def _reduce_paths(paths) -> list[PartRanges]:
    ranges = []
    for path in paths:
        reduced = PartRanges()
        for condition in path:
            new_range = _condition_to_range(condition)
            current_range = getattr(reduced, condition.attr)
            combined_range = _combine_ranges(current_range, new_range)
            setattr(reduced, condition.attr, combined_range)
        ranges.append(reduced)
    return ranges


def _sum_combinations(part_ranges: list[PartRanges]) -> int:
    return sum(
        [
            math.prod(
                range_.end - range_.start + 1
                for range_ in (part.x, part.m, part.a, part.s)
            )
            for part in part_ranges
        ]
    )


def distinct_combinations(workflows):
    accepted_paths = _walk_accepted_paths(workflows)
    ranges = _reduce_paths(accepted_paths)
    sum_combinations = _sum_combinations(ranges)
    return sum_combinations


def read_file() -> str:
    with open("input.txt") as f:
        return f.read()


def main():
    input_ = read_file()
    workflows, parts = parse_input(input_)
    sorted_parts = sort_through_parts(workflows, parts)
    print(
        "Sum of rating numbers for accepted parts:",
        sum_parts(sorted_parts),
    )
    print(
        f"Distinct combinations of ratings where each combination can be between {MIN_VALUE} and {MAX_VALUE}:",
        distinct_combinations(workflows),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
