from advent_of_code.year_2023.day_04 import process


def test_parse_cards():
    """
    Some scratchcards have ids of 2 or 3 digits
    Card ids are vertically stacked and right-aligned
    Ensure 1, 2 and 3 digit values can be parsed
    """
    scratchcard_input = """\
Card   1: 41 48 | 83 86  6
Card  12: 13 32 | 61 30 68
Card 376:  1 21 | 69 82 63"""
    scratchcards = process.Scratchcards(scratchcard_input)
    assert scratchcards.cards == {
        1: process.Card(winning_numbers={41, 48}, your_numbers={83, 86, 6}),
        12: process.Card(winning_numbers={13, 32}, your_numbers={61, 30, 68}),
        376: process.Card(winning_numbers={1, 21}, your_numbers={69, 82, 63}),
    }


def test_your_winning_numbers():
    scratchcard_input = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    scratchcards = process.Scratchcards(scratchcard_input)
    expected_your_winning_numbers = {
        1: {48, 83, 17, 86},
        2: {32, 61},
        3: {1, 21},
        4: {84},
        5: set(),
        6: set(),
    }
    your_winning_numbers = {
        id_: card.your_winning_numbers for id_, card in scratchcards.cards.items()
    }
    assert your_winning_numbers == expected_your_winning_numbers


def test_points():
    scratchcard_input = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    scratchcards = process.Scratchcards(scratchcard_input)
    points = scratchcards.points()
    assert points == {
        1: 8,
        2: 2,
        3: 2,
        4: 1,
        5: 0,
        6: 0,
    }
    assert process.sum_dict_values(points) == 13


def test_total_scratchcards():
    scratchcard_input = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    scratchcards = process.Scratchcards(scratchcard_input)
    total_scratchcards = scratchcards.total_scratchcards()
    assert total_scratchcards == {
        1: 1,
        2: 2,
        3: 4,
        4: 8,
        5: 14,
        6: 1,
    }
    assert process.sum_dict_values(total_scratchcards) == 30


def test_total_scratchcards_does_not_copy_cards_past_end_of_table():
    scratchcard_input = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19"""
    scratchcards = process.Scratchcards(scratchcard_input)
    total_scratchcards = scratchcards.total_scratchcards()
    assert total_scratchcards == {
        1: 1,
        2: 2,
    }
    assert process.sum_dict_values(total_scratchcards) == 3
