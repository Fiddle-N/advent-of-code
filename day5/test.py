from day5 import process


def test_FBFBBFFRLR_is_44_5():
    boarding_pass = 'FBFBBFFRLR'
    exp_seat = (44, 5)
    assert process.BinaryBoarding.process_pass(boarding_pass) == exp_seat
    assert process.BinaryBoarding.get_seat_id(exp_seat) == 357


def test_BFFFBBFRRR_is_70_7():
    boarding_pass = 'BFFFBBFRRR'
    exp_seat = (70, 7)
    assert process.BinaryBoarding.process_pass(boarding_pass) == exp_seat
    assert process.BinaryBoarding.get_seat_id(exp_seat) == 567


def test_FFFBBBFRRR_is_14_7():
    boarding_pass = 'FFFBBBFRRR'
    exp_seat = (14, 7)
    assert process.BinaryBoarding.process_pass(boarding_pass) == exp_seat
    assert process.BinaryBoarding.get_seat_id(exp_seat) == 119


def test_BBFFBBFRLL_is_102_4():
    boarding_pass = 'BBFFBBFRLL'
    exp_seat = (102, 4)
    assert process.BinaryBoarding.process_pass(boarding_pass) == exp_seat
    assert process.BinaryBoarding.get_seat_id(exp_seat) == 820