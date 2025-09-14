import itertools
import timeit


class FFT:
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


def main():
    input_val = read_file()

    fft = FFT(input_val)
    fft.process(100)
    print("8 digit output after 100 phases:", fft.signal)


if __name__ == "__main__":
    print("Time taken:", timeit.timeit(main, number=1))
