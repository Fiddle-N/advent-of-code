from advent_of_code.puzzles.year_2019.day_16 import process


def test_example_1():
    input_val = "12345678"
    fft = process.FFT(input_val)
    fft.process()
    assert fft.signal == "48226158"
    fft.process()
    assert fft.signal == "34040438"
    fft.process()
    assert fft.signal == "03415518"
    fft.process()
    assert fft.signal == "01029498"


def test_example_2():
    input_val = "80871224585914546619083218645595"
    fft = process.FFT(input_val)
    fft.process(100)
    assert fft.signal == "24176176"


def test_example_3():
    input_val = "19617804207202209144916044189917"
    fft = process.FFT(input_val)
    fft.process(100)
    assert fft.signal == "73745418"


def test_example_4():
    input_val = "69317163492948606335995924319873"
    fft = process.FFT(input_val)
    fft.process(100)
    assert fft.signal == "52432133"


def test_example_5():
    input_val = "03036732577212944063491565474664"
    fft = process.FFTXL(input_val)
    fft.process(100)
    assert fft.signal == "84462026"


def test_example_6():
    input_val = "02935109699940807407585447034323"
    fft = process.FFTXL(input_val)
    fft.process(100)
    assert fft.signal == "78725270"


def test_example_7():
    input_val = "03081770884921959731165446850517"
    fft = process.FFTXL(input_val)
    fft.process(100)
    assert fft.signal == "53553731"
