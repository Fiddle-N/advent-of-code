from more_itertools import chunked

from advent_of_code.common import read_file, timed_run

DISK_SIZE_1 = 272
DISK_SIZE_2 = 35651584


def generate_data(initial_data: str, target: int) -> list[str]:
    data = list(initial_data)
    while True:
        width = len(data)
        if width >= target:
            return data[:target]
        rev_data = reversed(["1" if x == "0" else "0" for x in data])
        data.append("0")
        data.extend(rev_data)


def generate_checksum(data: list[str]) -> str:
    while True:
        if len(data) % 2 == 1:
            return "".join(data)
        data = [("1" if a == b else "0") for a, b in chunked(data, 2, strict=True)]


def run():
    init_data = read_file()
    data = generate_data(initial_data=init_data, target=DISK_SIZE_1)
    print(generate_checksum(data))
    data = generate_data(initial_data=init_data, target=DISK_SIZE_2)
    print(generate_checksum(data))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
