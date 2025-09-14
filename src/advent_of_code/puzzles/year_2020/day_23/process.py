import timeit


def _get_destination_cup(cups, start):
    destination = start - 1
    while True:
        if destination in cups:
            return destination
        elif destination == 0:
            destination = max(cups)
        else:
            destination -= 1


def _crab_cups(cups, move_no):
    for move in range(move_no):
        cups = list(cups)
        start = cups[0]
        removed_cups = []
        for __ in range(3):
            removed_cups.append(cups.pop(1))
        destination = _get_destination_cup(cups, start)
        destination_idx = cups.index(destination)
        next_cups = (
            cups[: destination_idx + 1] + removed_cups + cups[destination_idx + 1 :]
        )
        next_cups.append(next_cups.pop(0))
        next_cups = tuple(next_cups)
        yield next_cups
        cups = next_cups


def crab_cups(cups, move_no):
    if isinstance(cups, str):
        cups = tuple(int(cup) for cup in cups)
    for move, x in enumerate(_crab_cups(cups, move_no)):
        yield x


def calculate_final_labels(cups):
    cups = list(cups)
    while cups[0] != 1:
        cups.append(cups.pop(0))
    return "".join(str(cup) for cup in cups[1:])


def main():
    with open("input.txt") as f:
        puzzle_input = f.read().strip()
    crab_cups_iter = crab_cups(puzzle_input, move_no=100)
    cups = None
    while True:
        try:
            cups = next(crab_cups_iter)
        except StopIteration:
            break
    print(f"Labels on cups after cup 1 for 100 rounds: {calculate_final_labels(cups)}")


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
