from advent_of_code.puzzles.year_2025.day_11 import process


def test_sum_total_paths_you():
    input_ = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
    device_map = process.parse(input_)
    solver = process.DeviceMapSolver(device_map)
    assert solver.sum_total_paths(start=process.YOU) == 5


def test_sum_total_paths_svr():
    input_ = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
    device_map = process.parse(input_)
    solver = process.DeviceMapSolver(device_map, check_dac_and_fft=False)
    assert solver.sum_total_paths(start=process.SERVER) == 8


def test_sum_total_paths_svr_including_dac_and_fft():
    input_ = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
    device_map = process.parse(input_)
    solver = process.DeviceMapSolver(device_map, check_dac_and_fft=True)
    assert solver.sum_total_paths(start=process.SERVER) == 2
