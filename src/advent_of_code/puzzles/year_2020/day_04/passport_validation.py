import re


def _is_valid_number(number, allow_leading_zeros=True):
    if not allow_leading_zeros and number[0] == '0':
        return False
    try:
        int(number)
    except ValueError:
        return False
    else:
        return True


def _is_number_between(number, start, end):
    number = int(number)
    return start <= number <= end


def _is_valid_number_between(year, start, end, allow_leading_zeros=False):
    return _is_valid_number(year, allow_leading_zeros) and _is_number_between(year, start, end)


def is_valid_birth_year(year):
    return _is_valid_number_between(year, start=1920, end=2002)


def is_valid_issue_year(year):
    return _is_valid_number_between(year, start=2010, end=2020)


def is_valid_expiration_year(year):
    return _is_valid_number_between(year, start=2020, end=2030)


def is_valid_height(height):
    height_re = re.fullmatch(r'(\d{2,3})(cm|in)', height)
    try:
        height_re.group(0)
    except AttributeError:
        return False
    length = height_re.group(1)
    system = height_re.group(2)
    if system == 'cm':
        return _is_valid_number_between(length, 150, 193, allow_leading_zeros=False)
    elif system == 'in':
        return _is_valid_number_between(length, 59, 76, allow_leading_zeros=False)
    else:
        raise Exception


def is_valid_hair_colour(hair_colour):
    if len(hair_colour) != 7:
        return False
    prefix, colour = hair_colour[:1], hair_colour[1:]
    if prefix != '#':
        return False
    try:
        int(colour, 16)
    except ValueError:
        return False
    else:
        return True


def is_valid_eye_colour(eye_colour):
    return eye_colour in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')


def is_valid_passport_id(passport_id):
    return len(passport_id) == 9 and _is_valid_number(passport_id, allow_leading_zeros=True)