from advent_of_code.puzzles.day_10 import process


def test_example_1():
    input_joltages = """\
16
10
15
5
1
11
7
19
6
12
4"""
    adapter_array = process.AdapterArray(input_joltages)
    assert adapter_array.jolts() == (7, 5)
    assert adapter_array.distinct_arrangements() == 8


def test_example_2():
    input_joltages = """\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
    adapter_array = process.AdapterArray(input_joltages)
    assert adapter_array.jolts() == (22, 10)
    assert adapter_array.distinct_arrangements() == 19208
