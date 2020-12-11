import math
import timeit

import more_itertools
import networkx as nx


class AdapterArray:

    def __init__(self, joltage_input=None):
        joltage_input = joltage_input if joltage_input is not None else self._read_file()
        self.joltage = [int(no) for no in joltage_input.splitlines()]
        self.joltage.append(0) # add wall outlet joltage
        self.joltage.append(max(self.joltage) + 3) # device built-in adapter
        self.joltage = sorted(self.joltage)

    @staticmethod
    def _read_file():
        with open('input.txt') as f:
            return f.read()

    def jolts(self):
        one_jolts = 0
        three_jolts = 0
        for lower_jolt, higher_jolt in more_itertools.windowed(self.joltage, 2):
            diff = higher_jolt - lower_jolt
            if diff == 1:
                one_jolts += 1
            elif diff == 3:
                three_jolts += 1
            else:
                raise Exception
        return one_jolts, three_jolts

    @staticmethod
    def _is_valid(path):
        for lower, upper in path:
            if upper - lower not in (1, 2, 3):
                return False
        return True

    @staticmethod
    def _arrangements(length):
        graph = nx.complete_graph(length, nx.DiGraph())
        paths = nx.all_simple_paths(graph, source=0, target=length-1)
        pairwise_paths = [nx.utils.pairwise(path) for path in paths]
        total = 0
        for path in pairwise_paths:
            is_valid_path = AdapterArray._is_valid(path)
            if is_valid_path:
                total += 1
        return total

    def distinct_arrangements(self):
        one_jolt_differences = more_itertools.split_when(self.joltage, lambda x, y: y - x == 3)
        one_jolt_difference_sections_greater_than_2 = [section for section in one_jolt_differences if len(section) > 2]
        section_lengths = [len(section) for section in one_jolt_difference_sections_greater_than_2]
        length_to_arrangement = {length: self._arrangements(length) for length in set(section_lengths)}
        arrangements = [length_to_arrangement[section_length] for section_length in section_lengths]
        return math.prod(arrangements)


def main():
    adapter_array = AdapterArray()
    one_jolts, three_jolts = adapter_array.jolts()
    print(f'1-jolt multiplied by 3-jolt differences: {one_jolts * three_jolts}')
    print(f'Adapter distinct arrangements: {adapter_array.distinct_arrangements()}')


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')