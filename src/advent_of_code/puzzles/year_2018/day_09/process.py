from collections import deque
from dataclasses import dataclass
from itertools import cycle
from re import fullmatch

from advent_of_code.common import read_file, timed_run


CONDITIONS_PATTERN = (
    r"(?P<n_players>\d+) players; last marble is worth (?P<last_marble_pts>\d+) points"
)


@dataclass(frozen=True)
class MarbleGameConditions:
    n_players: int
    last_marble_pts: int


def parse_game_conditions(raw_conditions: str) -> MarbleGameConditions:
    conditions_match = fullmatch(CONDITIONS_PATTERN, raw_conditions)
    assert conditions_match
    return MarbleGameConditions(
        int(conditions_match["n_players"]), int(conditions_match["last_marble_pts"])
    )


@dataclass
class Player:
    number: int
    score: int = 0


class MarbleGame:
    def __init__(self, conditions: MarbleGameConditions, marble_multiplier: int = 1):
        self.circle = deque()
        self.players = [Player(player_no) for player_no in range(conditions.n_players)]
        self.last_marble_pts = conditions.last_marble_pts * marble_multiplier

    def play(self) -> int:
        for marble, player in enumerate(cycle(self.players)):
            if marble and (marble % 23 == 0):
                self.circle.rotate(7)
                player.score += self.circle.pop() + marble
                self.circle.rotate(-1)
            else:
                self.circle.rotate(-1)
                self.circle.append(marble)
            if marble == self.last_marble_pts:
                return max(self.players, key=lambda player_: player_.score).score
        raise ValueError("Zero players is not allowed")


def run() -> None:
    raw_conditions = read_file()
    conditions = parse_game_conditions(raw_conditions)
    game_1 = MarbleGame(conditions)
    print(game_1.play())
    game_2 = MarbleGame(conditions, marble_multiplier=100)
    print(game_2.play())


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
