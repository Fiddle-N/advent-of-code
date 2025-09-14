from day_16 import process


def test_part_1():
    input_str = """\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    ticket_translation = process.TicketTranslation(input_str)
    result = ticket_translation.invalid_tickets()
    assert result == [4, 55, 12]
    assert sum(result) == 71
    assert ticket_translation.valid_tickets == [[7, 3, 47]]


def test_part_2():
    input_str = """\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""
    ticket_translation = process.TicketTranslation(input_str)
    ticket_translation.invalid_tickets()
    assert ticket_translation.valid_tickets == [[3, 9, 18], [15, 1, 5], [5, 14, 9]]
    assert ticket_translation.determine_fields() == ['row', 'class', 'seat']
