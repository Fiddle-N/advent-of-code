import ast
import itertools
import timeit

import regex


def parse(input_str):
    output = {}
    for line in input_str.splitlines():
        label, rule = line.split(": ")
        split_rule = rule.split(" | ")
        split_chars = []
        for rule in split_rule:
            chars = []
            for char in rule.split():
                try:
                    char_int = int(char)
                except ValueError:
                    chars = ast.literal_eval(char)  # parse literal string
                    break
                else:
                    chars.append(char_int)
            else:
                chars = tuple(chars)
            split_chars.append(chars)
        output_label = int(label)
        output[output_label] = split_chars
    return output


class CalculateRules:
    def __init__(self, parsed):
        self.parsed = parsed
        self.calculated = parsed
        self.calculated_cached = {}

    def calculate(self):
        while set(self.calculated.keys()) != set(self.calculated_cached.keys()):
            new_calculated = {}
            new_calculated_cache = {}
            for label, rule in self.calculated.items():
                new_rule = []
                for sub_rule in rule:
                    if isinstance(sub_rule, tuple):
                        results = self._calculate(sub_rule)
                        if results is None:
                            new_rule.append(sub_rule)
                        else:
                            new_rule.extend(results)
                    else:
                        new_rule.append(sub_rule)
                new_calculated[label] = new_rule
                if label not in self.calculated_cached:
                    if all(isinstance(sub_rule, str) for sub_rule in new_rule):
                        new_calculated_cache[label] = True
            self.calculated = new_calculated
            self.calculated_cached.update(new_calculated_cache)
        return self.calculated

    def _calculate(self, sub_rule):
        are_labels_calculated = all(
            self.calculated_cached.get(label, False) for label in sub_rule
        )
        if not are_labels_calculated:
            return None
        sub_rule_letters = [self.calculated[label] for label in sub_rule]
        return ["".join(result) for result in itertools.product(*sub_rule_letters)]


class MonsterMessages:
    def __init__(self, input_str):
        self.input_str = input_str
        raw_rules, raw_messages = input_str.split("\n\n")
        parsed_rules = parse(raw_rules)
        self.rules = CalculateRules(parsed_rules).calculate()
        self.messages = raw_messages.splitlines()

    def number_of_messages_that_match_rule_0(self):
        rule_0_rules = set(self.rules[0])
        matches = 0
        for message in self.messages:
            if message in rule_0_rules:
                matches += 1
        return matches

    def number_of_messages_that_match_rule_0_with_recursive_rules(self):
        pattern_42 = f"({'|'.join(self.rules[42])})"
        pattern_31 = f"({'|'.join(self.rules[31])})"
        pattern_8 = f"{pattern_42}+"  # match one or more of 42
        pattern_11 = f"(?P<pattern_11>{pattern_42}(?&pattern_11){pattern_31}|{pattern_42}{pattern_31})"  # matches exactly the same number of 42 and 31
        pattern_0 = pattern_8 + pattern_11

        matches = 0
        for message in self.messages:
            if regex.fullmatch(pattern_0, message):
                matches += 1
        return matches

    @classmethod
    def from_file(cls):
        with open("input.txt") as f:
            return cls(f.read())


def main():
    monster_messages = MonsterMessages.from_file()
    print(
        "Number of messages that completely match rule 0:",
        monster_messages.number_of_messages_that_match_rule_0(),
        sep=" ",
    )
    print(
        "Number of messages that completely match rule 0 with recursive rules:",
        monster_messages.number_of_messages_that_match_rule_0_with_recursive_rules(),
        sep=" ",
    )


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
