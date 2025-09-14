import collections
import timeit

import cProfile


def memory_game(start_seq, stop_val):
    counter = collections.defaultdict(list)
    start_list = [int(number) for number in start_seq.split(',')]
    turn = None
    turn_number = None
    for idx, turn_number in enumerate(start_list):
        turn = idx + 1
        counter[turn_number].append(turn)
    for turn in range(turn + 1, stop_val + 1):
        last_turn_number = turn_number
        if len(counter[last_turn_number]) > 1:  # number was twice spoken before
            turn_number_turns = counter[last_turn_number]
            turn_number = turn_number_turns[-1] - turn_number_turns[-2]
        else:   # number was only spoken once before
            assert len(counter[last_turn_number]) == 1
            turn_number = 0
        counter[turn_number].append(turn)
    return turn_number


def main():
    start = '0,13,1,8,6,15'
    print(f'For sequence {start} ; the 2020th value is {memory_game(start, 2020)}')
    print(f'For sequence {start} ; the 30 millionth value is {memory_game(start, 30_000_000)}')


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
