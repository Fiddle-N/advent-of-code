import timeit

import more_itertools


class EncodingError:
    def __init__(self, cypher_input=None):
        cypher_input = cypher_input if cypher_input is not None else self._read_file()
        self.cypher = [int(no) for no in cypher_input.splitlines()]

    @staticmethod
    def _read_file():
        with open("input.txt") as f:
            return f.read()

    @staticmethod
    def _first_number_not_total_of_previous_two(previous_numbers, total):
        for previous_number in previous_numbers:
            if previous_number >= total / 2:
                continue
            subtraction = total - previous_number
            if subtraction in previous_numbers:
                return True
        return False

    def first_number_not_total_of_previous_two(self, window_size):
        for window in more_itertools.windowed(self.cypher, window_size + 1):
            previous_numbers, total = window[:window_size], window[window_size:]
            (total,) = total
            result = self._first_number_not_total_of_previous_two(
                previous_numbers, total
            )
            if not result:
                return total

    def total_of_lowest_and_highest_in_contiguous_set(self, total):
        for i, _ in enumerate(self.cypher):
            resultant_cypher = self.cypher[i:]
            attempted_total = 0
            for j, number in enumerate(resultant_cypher):
                attempted_total += number
                if attempted_total == total:
                    result = resultant_cypher[: j + 1]
                    return min(result) + max(result)
                if attempted_total >= total:
                    break


def main():
    encoding_error = EncodingError()
    first_number_not_total_of_previous_two = (
        encoding_error.first_number_not_total_of_previous_two(window_size=25)
    )
    print(
        f"First number not the sum of two of the 25 numbers before it: {first_number_not_total_of_previous_two}"
    )
    print(
        f"Total of lowest and highest in contiguous set: "
        f"{encoding_error.total_of_lowest_and_highest_in_contiguous_set(first_number_not_total_of_previous_two)}"
    )


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
