from day_01 import process


def test_combo_2():
    input_list = [1721, 979, 366, 299, 675, 1456]
    assert process.process(input_list, combo_no=2) == 514579


def test_combo_3():
    input_list = [1721, 979, 366, 299, 675, 1456]
    assert process.process(input_list, combo_no=3) == 241861950