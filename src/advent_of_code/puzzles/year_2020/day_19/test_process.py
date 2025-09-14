from advent_of_code.puzzles.year_2020.day_19 import process


def test_one_level():
    input_rules = '''\
1: "a"
2: 1 3 | 3 1
3: "b"'''
    parsed = {
        1: ["a"],
        2: [(1, 3), (3, 1)],
        3: ["b"],
    }
    assert process.parse(input_rules) == parsed

    calculated = {
        1: ["a"],
        2: ["ab", "ba"],
        3: ["b"],
    }

    calculate_rules = process.CalculateRules(parsed)
    assert calculate_rules.calculate() == calculated


def test_two_levels():
    input_rules = '''\
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"'''
    parsed = {
        0: [(1, 2)],
        1: ["a"],
        2: [(1, 3), (3, 1)],
        3: ["b"],
    }
    assert process.parse(input_rules) == parsed

    calculated = {
        0: ["aab", "aba"],
        1: ["a"],
        2: ["ab", "ba"],
        3: ["b"],
    }

    calculate_rules = process.CalculateRules(parsed)
    assert calculate_rules.calculate() == calculated


def test_multiple_levels():
    input_rules = '''\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"'''
    parsed = {
        0: [(4, 1, 5)],
        1: [(2, 3), (3, 2)],
        2: [(4, 4), (5, 5)],
        3: [(4, 5), (5, 4)],
        4: ["a"],
        5: ["b"],
    }
    assert process.parse(input_rules) == parsed

    calculated = {
        0: [
            "aaaabb",
            "aaabab",
            "abbabb",
            "abbbab",
            "aabaab",
            "aabbbb",
            "abaaab",
            "ababbb",
        ],
        1: ["aaab", "aaba", "bbab", "bbba", "abaa", "abbb", "baaa", "babb"],
        2: ["aa", "bb"],
        3: ["ab", "ba"],
        4: ["a"],
        5: ["b"],
    }

    calculate_rules = process.CalculateRules(parsed)
    assert calculate_rules.calculate() == calculated


def test_apply_rules():
    input_str = """\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

    monster_messages = process.MonsterMessages(input_str)
    assert monster_messages.number_of_messages_that_match_rule_0() == 2


def test_apply_rules_2():
    input_str = """\
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

    monster_messages = process.MonsterMessages(input_str)
    assert (
        monster_messages.number_of_messages_that_match_rule_0_with_recursive_rules()
        == 12
    )
