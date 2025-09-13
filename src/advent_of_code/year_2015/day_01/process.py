
MAPPING = {'(': 1, ')': -1}

def read_file():
    with open('input.txt') as f:
        return f.read().strip()

def part1(text):
    floor = 0
    for char in text:
        floor += MAPPING[char]
    return floor


def part2(text):
    floor = 0
    for pos, char in enumerate(text):
        floor += MAPPING[char]
        if floor < 0:
            return pos + 1


if __name__ == '__main__':
    text = read_file()
    print(part1(text))
    print(part2(text))
