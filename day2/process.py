import timeit

def read():
    with open('input.txt') as f:
        return f.read()


def sled_rental_rule(password, char, lower_bound, upper_bound):
    char_count = password.count(char)
    if char_count != (len(password.split(char)) - 1):
        print(password)
    return lower_bound <= char_count <= upper_bound

def official_toboggan_rule(password, char, pos1, pos2):
    pos1_letter = password[pos1 - 1]
    pos2_letter = password[pos2 - 1]
    is_pos1_letter_correct = (pos1_letter == char)
    is_pos2_letter_correct = (pos2_letter == char)
    return is_pos1_letter_correct != is_pos2_letter_correct


def process(input_str):
    sled_rental_valid_passwords = 0
    official_toboggan_valid_passwords = 0
    for line in input_str.strip().split('\n'):
        rule, raw_char, password = line.split()
        char = raw_char[0]
        no1, no2 = rule.split('-')
        no1 = int(no1)
        no2 = int(no2)
        if sled_rental_rule(password, char, lower_bound=no1, upper_bound=no2):
            sled_rental_valid_passwords += 1
        if official_toboggan_rule(password, char, pos1=no1, pos2=no2):
            official_toboggan_valid_passwords += 1
    return sled_rental_valid_passwords, official_toboggan_valid_passwords


def main():
    input_str = read()
    sled_rental_valid_passwords, official_toboggan_valid_passwords = process(input_str)
    print(f'Valid sled rental passwords: {sled_rental_valid_passwords}')
    print(f'Valid official toboggan passwords: {official_toboggan_valid_passwords}')


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
