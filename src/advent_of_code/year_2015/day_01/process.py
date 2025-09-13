"""
2015 Day 1

Part 1
A string of () parentheses represents directions that Santa should go up and down floors in, where ( is go up one floor
and ) is go down one floor. If Santa enters at floor 0, find the floor he ends up in.

Part 2
Find the position in the directions where Santa enters the basement (floor -1).
"""


DIRECTION_MAPPING = {'(': 1, ')': -1}

def read_file():
    with open('input.txt') as f:
        return f.read().strip()

def traverse_floors(directions):
    floor = 0
    for direction in directions:
        floor += DIRECTION_MAPPING[direction]
    return floor


def find_position_that_enters_basement(directions):
    floor = 0
    for position, direction in enumerate(directions):
        floor += DIRECTION_MAPPING[direction]
        if floor < 0:
            return position + 1
    raise ValueError("Santa will always enter the basement")


def main():
    directions = read_file()
    print(traverse_floors(directions))
    print(find_position_that_enters_basement(directions))

if __name__ == '__main__':
    main()
