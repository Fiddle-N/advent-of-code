import pytest

from advent_of_code.puzzles.year_2018.day_09 import process


@pytest.mark.parametrize(
    "n_players,last_marble_pts,winning_score",
    [
        (9, 25, 32),
        (10, 1618, 8317),
        (13, 7999, 146373),
        (17, 1104, 2764),
        (21, 6111, 54718),
        (30, 5807, 37305),
    ],
)
def test_marble_game(n_players: int, last_marble_pts, winning_score: int) -> None:
    assert (
        process.play_marble_game(
            process.MarbleGameConditions(n_players, last_marble_pts)
        )
        == winning_score
    )
