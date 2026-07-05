from enum import Enum, auto
import heapq
from typing import Literal
from dataclasses import dataclass, field

from advent_of_code.common import read_file, timed_run

STARTING_MANA = 500
STARTING_HP = 50


class SpellType(Enum):
    MAGIC_MISSILE = auto()
    DRAIN = auto()
    SHIELD = auto()
    POISON = auto()
    RECHARGE = auto()


COSTS = {
    SpellType.MAGIC_MISSILE: 53,
    SpellType.DRAIN: 73,
    SpellType.SHIELD: 113,
    SpellType.POISON: 173,
    SpellType.RECHARGE: 229,
}


DURATION = {
    SpellType.SHIELD: 6,
    SpellType.POISON: 6,
    SpellType.RECHARGE: 5,
}


@dataclass(frozen=True)
class BossStats:
    hp: int
    damage: int


@dataclass(frozen=True, order=True)
class BattleState:
    spent_mana: int
    mana: int = field(compare=False)
    player_hp: int = field(compare=False)
    boss_hp: int = field(compare=False)
    shield_effect: int = field(compare=False)
    poison_effect: int = field(compare=False)
    recharge_effect: int = field(compare=False)
    next_turn: Literal["player", "boss"] = field(compare=False)


def battle(boss_stats: BossStats, hard_mode=False):
    states = []
    heapq.heappush(
        states,
        BattleState(
            spent_mana=0,
            mana=STARTING_MANA,
            player_hp=STARTING_HP,
            boss_hp=boss_stats.hp,
            shield_effect=0,
            poison_effect=0,
            recharge_effect=0,
            next_turn="player",
        ),
    )

    while True:
        state = heapq.heappop(states)

        # loss condition check
        player_hp = state.player_hp
        if player_hp <= 0:
            continue

        # win condition check
        boss_hp = state.boss_hp
        if boss_hp <= 0:
            return state.spent_mana

        if hard_mode and state.next_turn == "player":
            player_hp -= 1
            if player_hp <= 0:
                continue

        armour = 0
        mana = state.mana

        shield_effect = state.shield_effect
        poison_effect = state.poison_effect
        recharge_effect = state.recharge_effect

        # existing spells
        if shield_effect:
            armour = 7
            shield_effect -= 1

        if poison_effect:
            boss_hp -= 3
            # if poison kills the boss, register this immediately
            # do not allow the boss to cast any spells
            if boss_hp <= 0:
                return state.spent_mana
            poison_effect -= 1

        if recharge_effect:
            mana += 101
            recharge_effect -= 1

        if state.next_turn == "boss":
            turn_dmg = max(boss_stats.damage - armour, 1)
            heapq.heappush(
                states,
                BattleState(
                    spent_mana=state.spent_mana,
                    mana=mana,
                    player_hp=player_hp - turn_dmg,
                    boss_hp=boss_hp,
                    shield_effect=shield_effect,
                    poison_effect=poison_effect,
                    recharge_effect=recharge_effect,
                    next_turn="player",
                ),
            )
            continue

        for spell in SpellType:
            # cost check
            cost = COSTS[spell]
            if mana < cost:
                continue

            # existing spell checks
            if (
                (shield_effect and spell == SpellType.SHIELD)
                or (poison_effect and spell == SpellType.POISON)
                or (recharge_effect and spell == SpellType.RECHARGE)
            ):
                continue

            # new spells
            next_player_hp = player_hp
            next_boss_hp = boss_hp
            next_shield_effect = shield_effect
            next_poison_effect = poison_effect
            next_recharge_effect = recharge_effect

            match spell:
                case SpellType.MAGIC_MISSILE:
                    next_boss_hp -= 4
                case SpellType.DRAIN:
                    next_boss_hp -= 2
                    next_player_hp += 2
                case SpellType.SHIELD:
                    next_shield_effect = DURATION[spell]
                case SpellType.POISON:
                    next_poison_effect = DURATION[spell]
                case SpellType.RECHARGE:
                    next_recharge_effect = DURATION[spell]

            heapq.heappush(
                states,
                BattleState(
                    spent_mana=state.spent_mana + cost,
                    mana=mana - cost,
                    player_hp=next_player_hp,
                    boss_hp=next_boss_hp,
                    shield_effect=next_shield_effect,
                    poison_effect=next_poison_effect,
                    recharge_effect=next_recharge_effect,
                    next_turn="boss",
                ),
            )


def parse_boss_stats(raw_boss_stats: str) -> BossStats:
    boss_stats = [int(line.split(": ")[1]) for line in raw_boss_stats.splitlines()]
    return BossStats(hp=boss_stats[0], damage=boss_stats[1])


def run():
    raw_boss_stats = read_file()
    boss_stats = parse_boss_stats(raw_boss_stats)
    print(battle(boss_stats))
    print(battle(boss_stats, hard_mode=True))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
