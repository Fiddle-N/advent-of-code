import collections
import itertools
import timeit


def consume(iterator, n=None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(itertools.islice(iterator, n, n), None)


class FFT:
    BASE_PATTERN = (0, 1, 0, -1)

    def __init__(self, signal):
        self._signal = list(int(digit) for digit in signal)

    @property
    def signal(self):
        return "".join(str(x) for x in itertools.islice(self._signal, 8))

    def _last_digit(self, result):
        return int(str(result)[-1])

    def _calculate_result(self, pattern):
        result = 0
        for input_digit, pattern_digit in zip(self._signal, pattern):
            if not input_digit or not pattern_digit:
                continue
            result += input_digit * pattern_digit
        return result

    def _generate(self, idx):
        base_pattern = itertools.chain.from_iterable(
            itertools.repeat(digit, idx + 1) for digit in self.BASE_PATTERN
        )
        pattern = itertools.cycle(base_pattern)
        consume(pattern, n=1)
        result = self._calculate_result(pattern)
        return self._last_digit(result)

    def process(self, turns=1):
        for turn in range(turns):
            self._signal = [self._generate(idx) for idx, _ in enumerate(self._signal)]


class FFTXL:
    def __init__(self, signal, repeat=10000, offset_digits=7, output_digits=8):
        signal_length = len(signal) * repeat
        offset = int(signal[:offset_digits])
        position = offset / signal_length
        if position < 0.5:
            raise Exception("can only work out figures in the second half")
        self._signal = [int(digit) for digit in signal] * repeat
        self._signal = self._signal[offset:]
        self._output_digits = output_digits

    @property
    def signal(self):
        return "".join(
            str(digit) for digit in itertools.islice(self._signal, self._output_digits)
        )

    def _single_digit_add(self, input_1, input_2):
        intermediate = input_1 + input_2
        return intermediate % 10

    def process(self, turns=1):
        reverse_signal = reversed(self._signal)
        for turn in range(turns):
            reverse_signal = itertools.accumulate(
                reverse_signal, func=self._single_digit_add
            )
        self._signal = list(reversed(list(reverse_signal)))


def read_file():
    with open("input.txt") as f:
        return f.read().rstrip()


def main_1():
    input_val = read_file()

    fft = FFT(input_val)
    fft.process(100)
    print("First eight digits of output after 100 phases:", fft.signal)


def main_2():
    input_val = read_file()

    fft = FFTXL(input_val)
    fft.process(100)
    print("8 digit output after 100 phases:", fft.signal)


if __name__ == "__main__":
    print("Time taken:", timeit.timeit(main_1, number=1))
    print("Time taken:", timeit.timeit(main_2, number=1))
