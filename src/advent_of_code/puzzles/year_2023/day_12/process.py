import functools
import dataclasses
import re

# spring patterns
OPERATIONAL = r"\."
DAMAGED = "#"
UNKNOWN = r"\?"

MAYBE_OPERATIONAL = f"[{OPERATIONAL}{UNKNOWN}]"
MAYBE_DAMAGED = f"[{DAMAGED}{UNKNOWN}]"


@functools.cache
def arrangements(condition_record: str, damaged_springs: tuple[int, ...]) -> int:
    end_of_condition_record = len(damaged_springs) == 1

    if end_of_condition_record and "?" not in condition_record:
        # match on exact number of damaged springs
        # optionally surrounded by operational springs
        pattern = f"{OPERATIONAL}*{DAMAGED}{{{damaged_springs[0]}}}{OPERATIONAL}*"
        return bool(re.fullmatch(pattern, condition_record))

    option_1 = option_2 = 0

    # option 1 - try an exact number of damaged springs at the beginning
    # flipping any unknowns if necessary
    # At least one operational spring afterwards is needed
    if end_of_condition_record:
        # if at the end
        # all springs afterwards must be operational, not just one
        pattern = f"{MAYBE_DAMAGED}{{{damaged_springs[0]}}}{MAYBE_OPERATIONAL}*"
        option_1 = bool(re.fullmatch(pattern, condition_record))
    else:
        # if not at the end
        # only one immediate following spring must be operational
        # the rest may make up the rest of the pattern
        pattern = f"{MAYBE_DAMAGED}{{{damaged_springs[0]}}}{MAYBE_OPERATIONAL}"
        if re.match(pattern, condition_record):
            option_1 = arrangements(
                condition_record[damaged_springs[0] + 1 :], damaged_springs[1:]
            )

    # option 2 - try a single . at the beginning (if possible) and recurse
    if re.match(f"{MAYBE_OPERATIONAL}", condition_record):
        option_2 = arrangements(condition_record[1:], damaged_springs)

    return option_1 + option_2


@dataclasses.dataclass
class SpringRow:
    condition_record: str
    dmg_groups: list[int]

    def arrangements(self):
        return arrangements(self.condition_record, tuple(self.dmg_groups))


class Field:
    def __init__(self, field_input, unfolded=False):
        self.spring_rows = []
        for row in field_input.splitlines():
            condition_record_input, dmg_group_input = row.split()
            dmg_group = [int(num) for num in dmg_group_input.split(",")]
            if unfolded:
                condition_record_input = "?".join([condition_record_input] * 5)
                dmg_group = dmg_group * 5
            self.spring_rows.append(SpringRow(condition_record_input, dmg_group))

    def arrangements(self):
        return [row.arrangements() for row in self.spring_rows]


def read_file():
    with open("input.txt") as f:
        return f.read()


def main() -> None:
    field_input = read_file()
    folded_field = Field(field_input)
    print("Sum of all possible spring arrangements:", sum(folded_field.arrangements()))
    unfolded_field = Field(field_input, unfolded=True)
    print(
        "Sum of all possible spring arrangements unfolded:",
        sum(unfolded_field.arrangements()),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
