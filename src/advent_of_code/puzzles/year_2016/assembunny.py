from enum import StrEnum, auto
from dataclasses import dataclass


class InstrType(StrEnum):
    CPY = auto()
    INC = auto()
    DEC = auto()
    JNZ = auto()


@dataclass(frozen=True)
class Instruction:
    type: InstrType
    args: tuple[int | str] | tuple[int | str, int | str]


def parse(raw_instrs: str) -> list[Instruction]:
    instrs = []
    for raw_instr in raw_instrs.splitlines():
        instr_type, raw_instr_vals = raw_instr.split(maxsplit=1)
        raw_instr_vals = raw_instr_vals.split()
        assert len(raw_instr_vals) in (1, 2)

        instr_vals = []
        for val in raw_instr_vals:
            try:
                val = int(val)
            except ValueError:
                pass
            instr_vals.append(val)

        instrs.append(Instruction(type=InstrType(instr_type), args=tuple(instr_vals)))
    return instrs


def run(regs: dict[str, int], instrs: list[Instruction]) -> dict[str, int]:
    idx = 0
    while True:
        if idx < 0 or idx >= len(instrs):
            return regs
        instr = instrs[idx]
        match instr:
            case Instruction(InstrType.CPY, (val, register)):
                val = regs[val] if isinstance(val, str) else val
                regs[register] = val
                idx += 1

            case Instruction(InstrType.INC, (register,)):
                regs[register] += 1
                idx += 1

            case Instruction(InstrType.DEC, (register,)):
                regs[register] -= 1
                idx += 1

            case Instruction(InstrType.JNZ, (val, offset)):
                val = regs[val] if isinstance(val, str) else val
                if val != 0:
                    idx += offset
                else:
                    idx += 1
