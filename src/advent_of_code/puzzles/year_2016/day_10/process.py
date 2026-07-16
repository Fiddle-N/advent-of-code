import re
from typing import Self, Literal, cast
from collections import deque
from dataclasses import dataclass
from math import prod

from advent_of_code.common import read_file, timed_run

LOW_CHECK_VAL = 17
HIGH_CHECK_VAL = 61


SEND_PATTERN = r"value (?P<val>\d+) goes to bot (?P<bot_id>\d+)"
BOT_PATTERN = (
    r"bot (?P<bot_id>\d+)"
    r" gives low to (?P<low_dest_type>bot|output) (?P<low_dest_id>\d+)"
    r" and high to (?P<high_dest_type>bot|output) (?P<high_dest_id>\d+)"
)


@dataclass(frozen=True)
class Dest:
    type: Literal["bot", "output"]
    id: int


@dataclass(frozen=True)
class SendInstr:
    val: int
    dest: Dest


@dataclass(frozen=True)
class BotInstr:
    bot_id: int
    low: Dest
    high: Dest


@dataclass(frozen=True)
class BotDecision:
    bot_id: int
    low: int
    high: int


class Instructions:
    def __init__(self, send_instrs: list[SendInstr], bot_instrs: dict[int, BotInstr]):
        self.send_instrs = send_instrs
        self.bot_instrs = bot_instrs

    @classmethod
    def from_raw_instrs(cls, raw_instrs: str) -> Self:
        send_instrs = []
        bot_instrs = {}
        for raw_instr in raw_instrs.splitlines():
            if raw_instr.startswith("value"):
                match_ = re.fullmatch(SEND_PATTERN, raw_instr)
                assert match_
                send_instrs.append(
                    SendInstr(
                        val=int(match_["val"]),
                        dest=Dest(type="bot", id=int(match_["bot_id"])),
                    )
                )
            else:
                match_ = re.fullmatch(BOT_PATTERN, raw_instr)
                assert match_
                bot_id = int(match_["bot_id"])
                bot_instrs[bot_id] = BotInstr(
                    bot_id=bot_id,
                    low=Dest(
                        type=cast(Literal["bot", "output"], match_["low_dest_type"]),
                        id=int(match_["low_dest_id"]),
                    ),
                    high=Dest(
                        type=cast(Literal["bot", "output"], match_["high_dest_type"]),
                        id=int(match_["high_dest_id"]),
                    ),
                )
        return cls(send_instrs, bot_instrs)


class Bot:
    def __init__(
        self,
        bot_instr: BotInstr,
        to_process: deque[SendInstr],
    ):
        self.bot_instr = bot_instr
        self.to_process = to_process
        self._store = []

    def send(self, val: int) -> BotDecision | None:
        self._store.append(val)
        if len(self._store) < 2:
            return None
        low, high = sorted(self._store)
        self.to_process.append(SendInstr(val=low, dest=self.bot_instr.low))
        self.to_process.append(SendInstr(val=high, dest=self.bot_instr.high))
        return BotDecision(bot_id=self.bot_instr.bot_id, low=low, high=high)


def run_instrs(
    instrs: Instructions, low_check: int, high_check: int
) -> tuple[int, tuple[int, int, int]]:
    to_process = deque(instrs.send_instrs)
    bots = {
        bot_id: Bot(bot_instr, to_process)
        for bot_id, bot_instr in instrs.bot_instrs.items()
    }
    outputs = {}
    bot_id_check = None
    while to_process:
        send_instr = to_process.pop()
        if send_instr.dest.type == "output":
            outputs[send_instr.dest.id] = send_instr.val
        else:
            bot_id = send_instr.dest.id
            bot = bots[bot_id]
            bot_decision = bot.send(send_instr.val)
            if bot_decision is None:
                continue
            if (
                bot_id_check is None
                and bot_decision.low == low_check
                and bot_decision.high == high_check
            ):
                bot_id_check = bot_id
        if bot_id_check is not None and 0 in outputs and 1 in outputs and 2 in outputs:
            return (bot_id_check, (outputs[0], outputs[1], outputs[2]))
    raise Exception("Checks and outputs should be ready once all outputs are exhausted")


def run() -> None:
    raw_instrs = read_file()
    instrs = Instructions.from_raw_instrs(raw_instrs)
    bot_id_check, outputs = run_instrs(instrs, low_check=17, high_check=61)
    print(bot_id_check)
    print(prod(outputs))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
