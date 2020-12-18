from day_18 import process


def test_simple_with_mode_same_precedence():
    input_str = '1 + 2 * 3 + 4 * 5 + 6'
    assert process.process(input_str, mode='same_precedence') == 71


def test_simple_with_mode_addition_first():
    input_str = '1 + 2 * 3 + 4 * 5 + 6'
    assert process.process(input_str, mode='addition_first') == 231


def test_nested_0_with_mode_same_precedence():
    input_str = '1 + (2 * 3) + (4 * (5 + 6))'
    assert process.process(input_str, mode='same_precedence') == 51


def test_nested_0_with_mode_addition_first():
    input_str = '1 + (2 * 3) + (4 * (5 + 6))'
    assert process.process(input_str, mode='addition_first') == 51


def test_nested_1_with_mode_same_precedence():
    input_str = '2 * 3 + (4 * 5)'
    assert process.process(input_str, mode='same_precedence') == 26


def test_nested_1_with_mode_addition_first():
    input_str = '2 * 3 + (4 * 5)'
    assert process.process(input_str, mode='addition_first') == 46


def test_nested_2_with_mode_same_precedence():
    input_str = '5 + (8 * 3 + 9 + 3 * 4 * 3)'
    assert process.process(input_str, mode='same_precedence') == 437


def test_nested_2_with_mode_addition_first():
    input_str = '5 + (8 * 3 + 9 + 3 * 4 * 3)'
    assert process.process(input_str, mode='addition_first') == 1445


def test_nested_3_with_mode_same_precedence():
    input_str = '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'
    assert process.process(input_str, mode='same_precedence') == 12240


def test_nested_3_with_mode_addition_first():
    input_str = '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'
    assert process.process(input_str, mode='addition_first') == 669060


def test_nested_4_with_mode_same_precedence():
    input_str = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'
    assert process.process(input_str, mode='same_precedence') == 13632


def test_nested_4_with_mode_addition_first():
    input_str = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'
    assert process.process(input_str, mode='addition_first') == 23340