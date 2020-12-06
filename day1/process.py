import itertools
import math
import functools
import timeit

def read():
    input_list = []
    with open('input.txt') as f:
        for line in f:
            input_list.append(int(line))
    return input_list


def process(input_list, combo_no):
    for combo in itertools.combinations(input_list, combo_no):
        if sum(combo) == 2020:
            return math.prod(combo)


def main(combo_no):
    input_list = read()
    print(f'Combo {combo_no}: {process(input_list, combo_no)}')


if __name__ == '__main__':
    main_2 = functools.partial(main, 2)
    main_3 = functools.partial(main, 3)
    print(timeit.timeit(main_2, number=1), 'seconds')
    print(timeit.timeit(main_3, number=1), 'seconds')
