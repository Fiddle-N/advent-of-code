import collections
import operator
from collections import deque
from collections.abc import Generator
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Literal, cast

from advent_of_code.common import read_file, timed_run


class InstrType(StrEnum):
    SND = auto()
    SET = auto()
    ADD = auto()
    MUL = auto()
    MOD = auto()
    RCV = auto()
    JGZ = auto()


OPERATIONS = {
    InstrType.SET: lambda a, b: b,
    InstrType.ADD: operator.add,
    InstrType.MUL: operator.mul,
    InstrType.MOD: operator.mod,
}


class Reg(str):
    pass


class Val(int):
    pass


@dataclass
class Instr:
    type: InstrType
    args: list[Reg | Val]


class MonitoredDeque(deque):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.send_no = 0

    def appendleft(self, item):
        self.send_no += 1
        return super().appendleft(item)


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


def _run_duet(
    regs: dict[Reg, int],
    instrs: list[Instr],
    mode: Literal["sound", "duet"],
    send_q: collections.deque,
    receive_q: collections.deque,
) -> Generator[int | None, None, None]:
    idx = 0
    while True:
        if idx < 0 or idx >= len(instrs):
            return None
        instr = instrs[idx]
        match instr:
            case Instr(InstrType.SND, (arg,)):
                arg_val = regs.get(arg, 0) if isinstance(arg, Reg) else arg
                send_q.appendleft(arg_val)
                idx += 1
            case Instr(
                (
                    InstrType.SET | InstrType.ADD | InstrType.MUL | InstrType.MOD
                ) as instr_type,
                (Reg() as reg, operand),
            ):
                operand_val = (
                    regs.get(operand, 0) if isinstance(operand, Reg) else operand
                )
                regs[reg] = OPERATIONS[instr_type](regs.get(reg, 0), operand_val)
                idx += 1
            case Instr(InstrType.RCV, (Reg() as reg,)):
                if mode == "sound":
                    freq = regs.get(reg, 0)
                    if freq != 0:
                        yield receive_q[0]
                else:
                    while True:
                        try:
                            val = receive_q.pop()
                        except IndexError:
                            yield
                        else:
                            regs[reg] = val
                            break
                idx += 1
            case Instr(InstrType.JGZ, (condition, offset)):
                condition_val = (
                    regs.get(condition, 0) if isinstance(condition, Reg) else condition
                )
                offset_val = regs.get(offset, 0) if isinstance(offset, Reg) else offset
                if condition_val > 0:
                    idx += offset_val
                else:
                    idx += 1


def run_singlet(instrs: list[Instr]) -> int:
    q = deque()
    gen = _run_duet(regs={}, instrs=instrs, mode="sound", send_q=q, receive_q=q)
    result = cast(int, next(gen))
    return result


def run_duet(instrs: list[Instr]) -> int:
    queue_0_to_1 = MonitoredDeque()
    queue_1_to_0 = MonitoredDeque()

    gen_0 = _run_duet(
        regs={Reg("p"): 0},
        instrs=instrs,
        mode="duet",
        send_q=queue_0_to_1,
        receive_q=queue_1_to_0,
    )
    gen_1 = _run_duet(
        regs={Reg("p"): 1},
        instrs=instrs,
        mode="duet",
        send_q=queue_1_to_0,
        receive_q=queue_0_to_1,
    )

    gen_0_terminated = False
    gen_1_terminated = False
    while True:
        if not gen_0_terminated:
            try:
                next(gen_0)
            except StopIteration:
                gen_0_terminated = True

        if not gen_1_terminated:
            try:
                next(gen_1)
            except StopIteration:
                gen_1_terminated = True

        if (gen_0_terminated and gen_1_terminated) or (
            len(queue_0_to_1) == 0 and len(queue_1_to_0) == 0
        ):
            return queue_1_to_0.send_no


def run():
    raw_instrs = read_file()
    instrs = parse(raw_instrs)
    print(run_singlet(instrs=instrs))
    print(run_duet(instrs=instrs))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
