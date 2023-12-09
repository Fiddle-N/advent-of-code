import itertools


def history_from_str(seq_str):
    return [int(num) for num in seq_str.strip().split()]


def get_full_history(history):
    full_history = [history]
    seq = history
    while True:
        next_seq = [pair[1] - pair[0] for pair in itertools.pairwise(seq)]
        full_history.append(next_seq)
        if set(next_seq) == {0}:
            return full_history
        elif len(seq) == 1:
            raise ValueError(
                'Could not predict history - sequence does not reduce to regular sum'
            )
        seq = next_seq


def extrapolate_full_history(full_history):
    next_reversed_history = []
    reversed_history = reversed(full_history)

    zeros = next(reversed_history)
    assert set(zeros) == {0}
    next_zeros = zeros.copy()
    for _ in range(2):
        # set first and last new diff
        next_zeros.append(0)
    next_reversed_history.append(next_zeros)

    start_diff = end_diff = 0
    for seq in reversed_history:
        next_seq = seq.copy()

        first_num = seq[0]
        start_diff = first_num - start_diff
        next_seq.insert(0, start_diff)

        last_num = seq[-1]
        end_diff += last_num
        next_seq.append(end_diff)

        next_reversed_history.append(next_seq)

    return list(reversed(next_reversed_history))


def get_extrapolated_report(report_input):
    report = [history_from_str(history) for history in report_input.splitlines()]
    full_report = [get_full_history(history) for history in report]
    extrapolated_report = [extrapolate_full_history(full_history) for full_history in full_report]
    return extrapolated_report


def next_extrapolated_val(extrapolated_history):
    return extrapolated_history[0][-1]


def sum_next_extrapolated_vals(extrapolated_report):
    return sum(
        next_extrapolated_val(extrapolated_history)
        for extrapolated_history in extrapolated_report
    )


def prev_extrapolated_val(extrapolated_history):
    return extrapolated_history[0][0]


def sum_prev_extrapolated_vals(extrapolated_report):
    return sum(
        prev_extrapolated_val(extrapolated_history)
        for extrapolated_history in extrapolated_report
    )


def read_file():
    with open("input.txt") as f:
        return f.read()


def main() -> None:
    report_input = read_file()
    extrapolated_report = get_extrapolated_report(report_input)
    print(
        "Sum of next extrapolated values in report:",
        sum_next_extrapolated_vals(extrapolated_report),
    )
    print(
        "Sum of previous extrapolated values in report:",
        sum_prev_extrapolated_vals(extrapolated_report),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
