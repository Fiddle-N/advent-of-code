from advent_of_code.puzzles.year_2020.day_09 import process


def test():
    input_str = """\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
    encoding_error = process.EncodingError(cypher_input=input_str)
    assert encoding_error.first_number_not_total_of_previous_two(window_size=5) == 127
    assert encoding_error.total_of_lowest_and_highest_in_contiguous_set(127) == 62

