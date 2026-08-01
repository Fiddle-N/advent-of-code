import re

import lark

from advent_of_code.common import read_file, timed_run

STREAM_GRAMMAR = r"""
    # garbage characters can be anything
    GARBAGE_UNESC_TEXT : /.*?/
    
    # ! ignores the next character within garbage
    # So !! escapes the second !
    # Hence, before the closing angle bracket
    # you may have an even number of !s only
    GARBAGE_TEXT : GARBAGE_UNESC_TEXT /(?<!!)(!!)*?/
    GARBAGE : "<" [GARBAGE_TEXT] ">"
    
    # groups contain one or more comma-separated groups
    # or garbage pieces
    ?group_inner : group | GARBAGE
    group : "{" (group_inner ("," group_inner)*)? "}"
    
    ?start : group
"""


class StreamTransformer(lark.Transformer):
    group = list

    def GARBAGE(self, val) -> str:
        # remove cancelled characters, then slice off angle brackets
        return re.sub(r"!.", "", val)[1:-1]


stream_parser = lark.Lark(
    STREAM_GRAMMAR, parser="lalr", transformer=StreamTransformer()
)


def calculate_score(group, score: int = 0) -> int:
    score += 1
    if not group:
        return score
    subgroups_score = 0
    for subgroup in group:
        if isinstance(subgroup, list):
            subgroups_score += calculate_score(subgroup, score)
    return score + subgroups_score


def count_garbage(group) -> int:
    return sum(
        (len(subgroup) if isinstance(subgroup, str) else count_garbage(subgroup))
        for subgroup in group
    )


def run():
    text = read_file()
    group = stream_parser.parse(text)
    print(calculate_score(group))
    print(count_garbage(group))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
