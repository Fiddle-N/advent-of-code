from advent_of_code.puzzles.day_25 import process


def test_example():
    combo_breaker = process.ComboBreaker(card_pk=5764801, door_pk=17807724)
    assert combo_breaker.card_loop_size == 8
    assert combo_breaker.door_loop_size == 11
    assert combo_breaker.encryption_key == 14897079