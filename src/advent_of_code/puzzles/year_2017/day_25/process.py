import re
from dataclasses import dataclass
from enum import IntEnum, auto, StrEnum

from advent_of_code.common import read_file, timed_run

SUMMARY_RULES_PATTERN = (
    r"Begin in state (?P<start_state>\w)\.\n"
    r"Perform a diagnostic checksum after (?P<diagnostic_steps>\d+) steps\."
)

STATE_RULES_PATTERN = (
    r"In state (?P<state>\w):\n"
    r"  If the current value is 0:\n"
    r"    - Write the value (?P<if_zero_val>0|1)\.\n"
    r"    - Move one slot to the (?P<if_zero_move>left|right)\.\n"
    r"    - Continue with state (?P<if_zero_state>\w)\.\n"
    r"  If the current value is 1:\n"
    r"    - Write the value (?P<if_one_val>0|1)\.\n"
    r"    - Move one slot to the (?P<if_one_move>left|right)\.\n"
    r"    - Continue with state (?P<if_one_state>\w)\."
)


class TapeVal(IntEnum):
    ZERO = 0
    ONE = 1


class TapeMove(StrEnum):
    LEFT = auto()
    RIGHT = auto()


@dataclass(frozen=True)
class StateRule:
    if_zero_val: TapeVal
    if_zero_move: TapeMove
    if_zero_state: str
    if_one_val: TapeVal
    if_one_move: TapeMove
    if_one_state: str


@dataclass
class Blueprint:
    start_state: str
    diagnostic_steps: int
    state_rules: dict[str, StateRule]


def parse(raw_blueprint: str) -> Blueprint:
    raw_summary_rules, raw_state_rules = raw_blueprint.split("\n\n", maxsplit=1)

    summary_rules_match = re.fullmatch(SUMMARY_RULES_PATTERN, raw_summary_rules)
    assert summary_rules_match
    start_state = summary_rules_match["start_state"]
    diagnostic_steps = int(summary_rules_match["diagnostic_steps"])

    state_rules = {}
    for raw_state_rule in raw_state_rules.split("\n\n"):
        state_rule_match = re.fullmatch(STATE_RULES_PATTERN, raw_state_rule)
        assert state_rule_match

        state_rules[state_rule_match["state"]] = StateRule(
            if_zero_val=TapeVal(int(state_rule_match["if_zero_val"])),
            if_zero_move=TapeMove(state_rule_match["if_zero_move"]),
            if_zero_state=state_rule_match["if_zero_state"],
            if_one_val=TapeVal(int(state_rule_match["if_one_val"])),
            if_one_move=TapeMove(state_rule_match["if_one_move"]),
            if_one_state=state_rule_match["if_one_state"],
        )

    return Blueprint(start_state, diagnostic_steps, state_rules)


def execute(blueprint: Blueprint) -> int:
    tape: dict[int, TapeVal] = {}
    state = blueprint.start_state
    slot = 0
    for _ in range(blueprint.diagnostic_steps):
        state_rule = blueprint.state_rules[state]
        curr_val = tape.get(slot, TapeVal.ZERO)
        if curr_val == 0:
            next_val = state_rule.if_zero_val
            move = state_rule.if_zero_move
            state = state_rule.if_zero_state
        else:
            next_val = state_rule.if_one_val
            move = state_rule.if_one_move
            state = state_rule.if_one_state
        tape[slot] = next_val
        slot_offset = -1 if move == TapeMove.LEFT else 1
        slot += slot_offset
    return sum(val for slot, val in tape.items() if val == 1)


def run():
    raw_blueprint = read_file()
    blueprint = parse(raw_blueprint)
    print(execute(blueprint))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
