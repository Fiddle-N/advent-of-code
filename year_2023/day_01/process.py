import regex

WORD_LETTERS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def read_file() -> str:
    with open("input.txt") as f:
        return f.read()


def _get_cal_val(line: str, include_word_numbers: bool) -> int:
    digit_pattern_vals = [r'\d']
    if include_word_numbers:
        digit_pattern_vals += list(WORD_LETTERS)
    digit_pattern = '|'.join(digit_pattern_vals)
    digits = regex.findall(digit_pattern, line, overlapped=True)
    mapped_digits = [WORD_LETTERS.get(digit, digit) for digit in digits]
    return int(mapped_digits[0] + mapped_digits[-1])


def sum_cal_vals(cal_doc: str, include_word_numbers: bool) -> int:
    cal_doc_list = cal_doc.splitlines()
    return sum(_get_cal_val(line, include_word_numbers) for line in cal_doc_list)


def main() -> None:
    cal_doc = read_file()
    print(
        "Sum of all calibration values, not counting word letters :",
        sum_cal_vals(cal_doc, include_word_numbers=False),
    )
    print(
        "Sum of all calibration values, counting word letters :",
        sum_cal_vals(cal_doc, include_word_numbers=True),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
