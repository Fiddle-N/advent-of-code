from day6 import process


def test_questions_anyone_answered():
    input_str = """\
abc

a
b
c

ab
ac

a
a
a
a

b"""
    custom_customs = process.CustomCustoms(input_str)
    assert custom_customs.questions_answered('anyone') == 11


def test_questions_everyone_answered():
    input_str = """\
abc

a
b
c

ab
ac

a
a
a
a

b"""
    custom_customs = process.CustomCustoms(input_str)
    assert custom_customs.questions_answered('everyone') == 6
