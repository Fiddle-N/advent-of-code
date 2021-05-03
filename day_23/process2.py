import timeit
import more_itertools


class CrabCups:

    def __init__(self, input, number_of_cups=1_000_000, moves=10_000_000):
        initial_cup_list = [int(x) for x in input]
        initial_max_cups = max(initial_cup_list)
        if number_of_cups is not None:
            cup_list = initial_cup_list + list(range(initial_max_cups + 1, number_of_cups + 1))
        else:
            cup_list = initial_cup_list
        self.max_cups = max(cup_list)
        self.cups = {}
        for cup, next_cup in more_itertools.windowed(cup_list, 2):
            self.cups[cup] = next_cup
        self.cups[cup_list[-1]] = cup_list[0]       # tie up last cup and first cup
        self.moves = moves

    @staticmethod
    def _to_be_removed(cups, current):
        removed = []
        for __ in range(3):
            adjacent = cups[current]
            removed.append(adjacent)
            current = adjacent
        return removed

    def _get_destination_cup(self, current, removed):
        destination = current - 1
        while True:
            if destination == 0:
                destination = self.max_cups
            if destination not in removed:
                return destination
            destination -= 1

    def process(self):
        cups = self.cups.copy()
        current = next(iter(cups))
        for move in range(self.moves):
            removed = self._to_be_removed(cups, current)
            destination = self._get_destination_cup(current, removed)

            # remove cups next to current cup
            adjacent_to_removed = cups[removed[-1]]
            cups[current] = adjacent_to_removed

            # insert removed cups next to destination cup
            adjacent_to_destination = cups[destination]
            cups[destination] = removed[0]
            cups[removed[-1]] = adjacent_to_destination

            current = adjacent_to_removed
        cup_1 = cups[1]
        cup_2 = cups[cup_1]
        return cup_1, cup_2


def main():
    with open('input.txt') as f:
        puzzle_input = f.read().strip()
    crab_cups = CrabCups(puzzle_input)
    result_cups = crab_cups.process()
    print('Result cups:', result_cups)
    print('Result cups multiplied:', result_cups[0] * result_cups[1])


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
