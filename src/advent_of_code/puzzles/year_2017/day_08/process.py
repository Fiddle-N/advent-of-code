import re
from dataclasses import dataclass

from advent_of_code.common import Operator, OP_FNS
from advent_of_code.common import read_file, timed_run

INSTR_PATTERN = (
    r"(?P<reg>\w+)"
    r" (?P<offset_sign>inc|dec)"
    r" (?P<offset>-?\d+)"
    r" if (?P<condition_reg>\w+)"
    rf" (?P<condition_op>{'|'.join(op.value for op in Operator)})"
    r" (?P<condition_operand>-?\d+)"
)


@dataclass(frozen=True)
class Instruction:
    reg: str
    offset: int
    condition_reg: str
    condition_op: Operator
    condition_operand: int


def parse_instrs(raw_instrs: str) -> list[Instruction]:
    instrs = []
    for raw_instr in raw_instrs.splitlines():
        match = re.fullmatch(INSTR_PATTERN, raw_instr)
        assert match
        offset_sign = -1 if match["offset_sign"] == "dec" else 1
        offset = int(match["offset"]) * offset_sign
        instrs.append(
            Instruction(
                reg=match["reg"],
                offset=offset,
                condition_reg=match["condition_reg"],
                condition_op=Operator(match["condition_op"]),
                condition_operand=int(match["condition_operand"]),
            )
        )
    return instrs


def run_instrs(instrs: list[Instruction]) -> tuple[int, int]:
    regs = {}
    max_val = None
    for instr in instrs:
        condition_operand_1 = regs.get(instr.condition_reg, 0)
        condition_fn = OP_FNS[instr.condition_op]
        result = condition_fn(condition_operand_1, instr.condition_operand)
        if not result:
            continue
        reg_val = regs.get(instr.reg, 0)
        reg_result = reg_val + instr.offset
        if max_val is None or reg_result > max_val:
            max_val = reg_result
        regs[instr.reg] = reg_result
    assert max_val is not None
    return max(regs.values()), max_val


def run():
    raw_instrs = read_file()
    instrs = parse_instrs(raw_instrs)
    result = run_instrs(instrs)
    print(result)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
