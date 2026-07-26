from enum import StrEnum, auto
from collections import deque
from dataclasses import dataclass


class InstrType(StrEnum):
    # assembunny instructions
    CPY = auto()
    INC = auto()
    DEC = auto()
    JNZ = auto()
    TGL = auto()

    # optimisation instructions
    MUL = auto()
    NOP = auto()


@dataclass(frozen=True)
class Instruction:
    type: InstrType
    args: tuple


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


def _is_optimisable_jnz(jnz: Instruction) -> bool:
    return (
        isinstance(jnz.args[0], str)
        and isinstance(jnz.args[1], int)
        and jnz.args[1] < 0
    )


def _optimise(instrs: list[Instruction]) -> list[Instruction]:
    optimised = instrs.copy()
    jnz_instrs = deque(
        [
            (idx, instr)
            for idx, instr in enumerate(optimised)
            if instr.type == InstrType.JNZ
        ]
    )
    while jnz_instrs:
        jnz_instr = jnz_instrs.pop()
        idx, instr = jnz_instr
        instr_val = instr.args[0]
        instr_offset = instr.args[1]

        if not (_is_optimisable_jnz(instr)):
            continue

        seq = optimised[idx + instr_offset : idx]
        if any(
            seq_instr.type == InstrType.JNZ and _is_optimisable_jnz(seq_instr)
            for seq_instr in seq
        ):
            jnz_instrs.appendleft(jnz_instr)
            continue

        # case 1 - optimise simple mul cases
        if (
            len(seq) == 2
            and (
                (loop_instr := Instruction(InstrType.INC, (instr_val,))) in seq
                or (loop_instr := Instruction(InstrType.DEC, (instr_val,))) in seq
            )
            and (changing_instr_set := set(seq).difference([loop_instr]))
            and (changing_instr := next(iter(changing_instr_set)))
            and changing_instr.type in (InstrType.INC, InstrType.DEC)
        ):
            new_instr_loop_sign = -1 if loop_instr.type == InstrType.INC else 1

            new_instr_loop_register = instr_val
            new_instr_changing_register = changing_instr.args[0]
            new_instr = Instruction(
                type=InstrType.MUL,
                args=(
                    ((new_instr_loop_register, new_instr_loop_sign),),
                    new_instr_changing_register,
                    (-1 if changing_instr.type == InstrType.DEC else 1),
                ),
            )

            # amend instructions whilst keeping same length
            optimised[idx - 2] = Instruction(type=InstrType.NOP, args=())
            optimised[idx - 1] = Instruction(type=InstrType.NOP, args=())
            optimised[idx] = new_instr

        # case 2 - optimise a nested mul case
        if (
            len(seq) == 5
            and (copy_instr := seq[0]).type == InstrType.CPY
            and (mul_instr := seq[3]).type == InstrType.MUL
            and (loop_instr := seq[4]).type in (InstrType.INC, InstrType.DEC)
        ):
            new_instr_loop_sign = -1 if loop_instr.type == InstrType.INC else 1
            new_instr = Instruction(
                type=InstrType.MUL,
                args=(
                    (mul_instr.args[0][0], (loop_instr.args[0], new_instr_loop_sign)),
                    mul_instr.args[1],
                    mul_instr.args[2],
                ),
            )

            # amend instructions whilst keeping same length
            optimised[idx - 4] = copy_instr
            optimised[idx - 3] = Instruction(type=InstrType.NOP, args=())
            optimised[idx - 2] = Instruction(type=InstrType.NOP, args=())
            optimised[idx - 1] = Instruction(type=InstrType.NOP, args=())
            optimised[idx] = new_instr

    return optimised


def _tgl(regs: dict[str, int], instrs: list[Instruction], idx: int, register: str):
    instr_idx = idx + regs[register]
    try:
        instr = instrs[instr_idx]
    except IndexError:
        return
    match instr:
        case Instruction(instr_type, (arg,)):
            instrs[instr_idx] = Instruction(
                type=InstrType.DEC if instr_type == InstrType.INC else InstrType.INC,
                args=(arg,),
            )
        case Instruction(
            instr_type,
            (
                arg_1,
                arg_2,
            ),
        ):
            instrs[instr_idx] = Instruction(
                type=InstrType.CPY if instr_type == InstrType.JNZ else InstrType.JNZ,
                args=(arg_1, arg_2),
            )


def run(regs: dict[str, int], instrs: list[Instruction]) -> dict[str, int]:
    instrs = instrs.copy()
    optimised = _optimise(instrs)

    idx = 0
    while True:
        if idx < 0 or idx >= len(optimised):
            return regs
        instr = optimised[idx]
        match instr:
            case Instruction(InstrType.CPY, (val, register)):
                val = regs[val] if isinstance(val, str) else val
                try:
                    regs[register] = val
                except ValueError:
                    pass
                idx += 1

            case Instruction(InstrType.INC, (register,)):
                try:
                    regs[register] += 1
                except ValueError:
                    pass
                idx += 1

            case Instruction(InstrType.DEC, (register,)):
                try:
                    regs[register] -= 1
                except ValueError:
                    pass
                idx += 1

            case Instruction(InstrType.JNZ, (val, offset)):
                val = regs[val] if isinstance(val, str) else val
                offset = regs[offset] if isinstance(offset, str) else offset
                if val != 0:
                    idx += offset
                else:
                    idx += 1

            case Instruction(InstrType.TGL, (register,)):
                _tgl(regs, instrs, idx, register)

                # reoptimise as optimised assumptions may no longer hold
                optimised = _optimise(instrs)

                idx += 1

            case Instruction(InstrType.MUL, (loop_registers, changing_register, sign)):
                loop_val_prod = 1
                for loop_register, loop_sign in loop_registers:
                    loop_val = regs[loop_register]
                    if loop_sign == 1:
                        assert loop_val > 0
                    if loop_sign == -1:
                        assert loop_val < 0
                    loop_val_prod *= loop_val

                regs[changing_register] += abs(loop_val_prod) * sign
                for loop_register, sign in loop_registers:
                    regs[loop_register] = 0

                idx += 1

            case Instruction(InstrType.NOP, _):
                idx += 1
