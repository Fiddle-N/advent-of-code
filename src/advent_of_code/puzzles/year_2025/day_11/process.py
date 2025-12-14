import functools

from advent_of_code.common import read_file, timed_run

YOU = "you"
SERVER = "svr"
DAC = "dac"
FFT = "fft"
TARGET = "out"


def parse(raw_input: str) -> dict[str, list[str]]:
    device_map = {}
    for line in raw_input.splitlines():
        device, raw_output = line.split(": ")
        outputs = raw_output.split()
        device_map[device] = outputs
    return device_map


class DeviceMapSolver:
    def __init__(self, device_map: dict[str, list[str]], check_dac_and_fft=False):
        self._device_map = device_map
        self._check_dac_and_fft = check_dac_and_fft

    @functools.cache
    def sum_total_paths(self, start=YOU, dac_found=False, fft_found=False):
        if start == TARGET:
            return 1 if not self._check_dac_and_fft or (dac_found and fft_found) else 0
        total = 0
        for output in self._device_map[start]:
            total += self.sum_total_paths(
                output,
                dac_found=dac_found or start == DAC,
                fft_found=fft_found or start == FFT,
            )
        return total


def run():
    device_map = parse(read_file())
    solver = DeviceMapSolver(device_map)
    print(solver.sum_total_paths(start=YOU))
    solver_2 = DeviceMapSolver(device_map, check_dac_and_fft=True)
    print(solver_2.sum_total_paths(start=SERVER))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
