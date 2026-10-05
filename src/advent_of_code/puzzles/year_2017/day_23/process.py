import operator
from enum import StrEnum, auto
from dataclasses import dataclass

from advent_of_code.common import read_file, timed_run


class InstrType(StrEnum):
    SET = auto()
    SUB = auto()
    MUL = auto()
    JNZ = auto()


OPERATIONS = {
    InstrType.SET: lambda a, b: b,
    InstrType.SUB: operator.sub,
    InstrType.MUL: operator.mul,
}


class Reg(str):
    pass


class Val(int):
    pass


@dataclass
class Instr:
    type: InstrType
    args: list[Reg | Val]


def parse(raw_instrs: str) -> list[Instr]:
    instrs = []
    for raw_instr in raw_instrs.splitlines():
        raw_type, *raw_args = raw_instr.split()
        args = []
        for raw_arg in raw_args:
            try:
                arg = Val(raw_arg)
            except ValueError:
                arg = Reg(raw_arg)
            args.append(arg)
        instrs.append(Instr(type=InstrType(raw_type), args=args))
    return instrs


def execute(
    regs: dict[Reg, int],
    instrs: list[Instr],
) -> int:
    idx = 0
    mul_invokes = 0
    while True:
        if idx < 0 or idx >= len(instrs):
            return mul_invokes
        instr = instrs[idx]
        match instr:
            case Instr(
                (InstrType.SET | InstrType.SUB | InstrType.MUL) as instr_type,
                (Reg() as reg, operand),
            ):
                if instr_type == InstrType.MUL:
                    mul_invokes += 1
                operand_val = (
                    regs.get(operand, 0) if isinstance(operand, Reg) else operand
                )
                regs[reg] = OPERATIONS[instr_type](regs.get(reg, 0), operand_val)
                idx += 1
            case Instr(InstrType.JNZ, (condition, offset)):
                condition_val = (
                    regs.get(condition, 0) if isinstance(condition, Reg) else condition
                )
                offset_val = regs.get(offset, 0) if isinstance(offset, Reg) else offset
                if condition_val != 0:
                    idx += offset_val
                else:
                    idx += 1


def run():
    raw_instrs = read_file()
    instrs = parse(raw_instrs)
    print(execute(regs={}, instrs=instrs))
    print(execute(regs={Reg("a"): 1}, instrs=instrs))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
