from itertools import tee


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def meets_criteria_1(number):
    digits = [int(digit) for digit in str(number)]
    double_digits = 0
    for digit, next_digit in pairwise(digits):
        if digit > next_digit:
            return False
        if digit == next_digit:
            double_digits += 1
    return double_digits


def meets_criteria_2(number):
    digits = [int(digit) for digit in str(number)]
    repeated_digits = 0
    meets_repeated_criteria = False
    for digit, next_digit in pairwise(digits):
        if digit > next_digit:
            return False
        if digit == next_digit:
            repeated_digits += 1
        else:
            if repeated_digits == 1:
                meets_repeated_criteria = True
            repeated_digits = 0
    if repeated_digits == 1:
        meets_repeated_criteria = True
    return meets_repeated_criteria


def check_passwords(fn, start, stop):
    count = 0
    for number in range(start, stop + 1):
        if fn(number):
            count += 1
    return count


def main():
    print(
        "Number of passwords that meet criteria 1 in range 158126-624574: "
        f"{check_passwords(meets_criteria_1, 158126, 624574)}"
    )
    print(
        "Number of passwords that meet criteria 2 in range 158126-624574: "
        f"{check_passwords(meets_criteria_2, 158126, 624574)}"
    )


if __name__ == "__main__":
    main()
