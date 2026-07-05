from dataclasses import dataclass

from advent_of_code.common import read_file, timed_run


@dataclass(frozen=True)
class Hlf:
    register: str


@dataclass(frozen=True)
class Tpl:
    register: str


@dataclass(frozen=True)
class Inc:
    register: str


@dataclass(frozen=True)
class Jmp:
    offset: int


@dataclass(frozen=True)
class Jie:
    register: str
    offset: int


@dataclass(frozen=True)
class Jio:
    register: str
    offset: int


type Instruction = Hlf | Tpl | Inc | Jmp | Jie | Jio


def parse_instrs(raw_instrs: str) -> list[Instruction]:
    instrs = []
    for raw_instr in raw_instrs.splitlines():
        instr_type, instr_vals = raw_instr.split(maxsplit=1)
        match instr_type:
            case "hlf":
                instr = Hlf(register=instr_vals)
            case "tpl":
                instr = Tpl(register=instr_vals)
            case "inc":
                instr = Inc(register=instr_vals)
            case "jmp":
                instr = Jmp(offset=int(instr_vals))
            case "jie":
                reg, offset = instr_vals.split(", ")
                instr = Jie(register=reg, offset=int(offset))
            case "jio":
                reg, offset = instr_vals.split(", ")
                instr = Jio(register=reg, offset=int(offset))
        instrs.append(instr)
    return instrs


def run_program(regs: dict[str, int], instrs: list[Instruction]) -> dict[str, int]:
    idx = 0
    while True:
        if idx < 0 or idx >= len(instrs):
            return regs
        instr = instrs[idx]
        match instr:
            case Hlf():
                regs[instr.register] //= 2
                idx += 1
            case Tpl():
                regs[instr.register] *= 3
                idx += 1
            case Inc():
                regs[instr.register] += 1
                idx += 1
            case Jmp():
                idx += instr.offset
            case Jie():
                if regs[instr.register] % 2 == 0:
                    idx += instr.offset
                else:
                    idx += 1
            case Jio():
                if regs[instr.register] == 1:
                    idx += instr.offset
                else:
                    idx += 1


def run():
    raw_instrs = read_file()
    instrs = parse_instrs(raw_instrs)

    init_regs = {
        "a": 0,
        "b": 0,
    }
    regs = run_program(init_regs, instrs)
    print(regs["b"])

    init_regs = {
        "a": 1,
        "b": 0,
    }
    regs = run_program(init_regs, instrs)
    print(regs["b"])


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
