"""
2015 Day 10

Look-and-say - read aloud the previous sequence and use that as the next. 1211 = 111221 (one 1, one 2, two 1s).

Part 1
Take the input and run 40 times.

Part 2
Take the input and run 50 times.
"""

import itertools

from advent_of_code.common import read_file, timed_run

PART_1_N = 40
PART_2_N = 50


def execute_look_and_say(input_num: str) -> str:
    grouped_input = [list(g) for _, g in itertools.groupby(input_num)]
    output_seq = []
    for group in grouped_input:
        output_seq.append(str(len(group)))
        output_seq.append(group[0])
    return "".join(output_seq)


def run() -> None:
    original_input_num = read_file()
    input_num = original_input_num
    for i in range(1, PART_2_N + 1):
        output = execute_look_and_say(input_num)
        if i == PART_1_N:
            print(len(output))
        input_num = output
    print(len(output))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
