from advent_of_code.common import read_file, timed_run

KEY_GROUP = 0


def parse_rels(raw_rels: str) -> list[list[int]]:
    rels = []
    for raw_rel in raw_rels.splitlines():
        _, raw_targets = raw_rel.split(" <-> ")
        rels.append([int(program) for program in raw_targets.split(", ")])
    return rels


def calculate_group(group: int, rels: list[list[int]]) -> set[int]:
    seen = set()
    remaining = [group]
    while remaining:
        program = remaining.pop()
        if program in seen:
            continue
        seen.add(program)
        remaining.extend(rels[program])
    return seen


def calculate_group_info(rels: list[list[int]]):
    remaining = set(idx for idx, _ in enumerate(rels))
    curr = KEY_GROUP
    total_groups = 0
    while True:
        curr_group = calculate_group(curr, rels)
        if curr == KEY_GROUP:
            key_group_length = len(curr_group)
        total_groups += 1
        remaining -= curr_group
        if not remaining:
            return key_group_length, total_groups
        curr = remaining.pop()


def run():
    raw_rels = read_file()
    rels = parse_rels(raw_rels)
    print(calculate_group_info(rels))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
