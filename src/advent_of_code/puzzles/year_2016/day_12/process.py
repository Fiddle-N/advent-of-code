from dataclasses import dataclass

from advent_of_code.common import read_file, timed_run


@dataclass(frozen=True)
class Cpy:
    val: str | int
    register: str


@dataclass(frozen=True)
class Inc:
    register: str


@dataclass(frozen=True)
class Dec:
    register: str


@dataclass(frozen=True)
class Jnz:
    val: str | int
    offset: int


type Instruction = Cpy | Inc | Dec | Jnz


def parse_instrs(raw_instrs: str) -> list[Instruction]:
    instrs = []
    for raw_instr in raw_instrs.splitlines():
        instr_type, instr_vals = raw_instr.split(maxsplit=1)
        match instr_type:
            case "cpy":
                val, register = instr_vals.split()
                try:
                    val = int(val)
                except ValueError:
                    pass
                instr = Cpy(val=val, register=register)
            case "inc":
                instr = Inc(register=instr_vals)
            case "dec":
                instr = Dec(register=instr_vals)
            case "jnz":
                val, offset = instr_vals.split()
                try:
                    val = int(val)
                except ValueError:
                    pass
                instr = Jnz(val=val, offset=int(offset))
        instrs.append(instr)
    return instrs


def run_program(regs: dict[str, int], instrs: list[Instruction]) -> dict[str, int]:
    idx = 0
    while True:
        if idx < 0 or idx >= len(instrs):
            return regs
        instr = instrs[idx]
        match instr:
            case Cpy():
                val = regs[instr.val] if isinstance(instr.val, str) else instr.val
                regs[instr.register] = val
                idx += 1
            case Inc():
                regs[instr.register] += 1
                idx += 1
            case Dec():
                regs[instr.register] -= 1
                idx += 1
            case Jnz():
                val = regs[instr.val] if isinstance(instr.val, str) else instr.val
                if val != 0:
                    idx += instr.offset
                else:
                    idx += 1


def run():
    raw_instrs = read_file()
    instrs = parse_instrs(raw_instrs)

    init_regs = {"a": 0, "b": 0, "c": 0, "d": 0}
    regs = run_program(init_regs, instrs)
    print(regs["a"])

    init_regs = {"a": 0, "b": 0, "c": 1, "d": 0}
    regs = run_program(init_regs, instrs)
    print(regs["a"])


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
