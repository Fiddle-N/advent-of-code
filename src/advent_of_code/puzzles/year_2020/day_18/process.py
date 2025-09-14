import collections
import string
import operator
import timeit


def parse(expr):
    def _parse(iter):
        items = []
        for item in iter:
            if item == "(":
                result, closeparen = _parse(iter)
                if not closeparen:
                    raise ValueError("bad expression -- unbalanced parentheses")
                items.append(result)
            elif item == ")":
                return items, True
            elif item in string.whitespace:
                continue
            else:
                try:
                    item = int(item)
                except ValueError:
                    if item not in ("+", "*"):
                        raise
                items.append(item)
        return items, False

    return _parse(iter(expr))[0]


def calculate(parsed, mode):
    operators = {
        "+": operator.add,
        "*": operator.mul,
    }

    def reduce_stack_same_precedence_mode(stack):
        while len(stack) > 1:
            l_operand = stack.popleft()
            operator = stack.popleft()
            r_operand = stack.popleft()
            result = operators[operator](l_operand, r_operand)
            stack.appendleft(result)
        return stack

    def reduce_stack_addition_first_mode(stack):
        new_stack = collections.deque()

        while stack:
            l_operand = stack.popleft()
            try:
                operator = stack.popleft()
            except IndexError:  # only one element in the original stack
                new_stack.append(l_operand)
            else:
                if operator == "*":
                    new_stack.append(l_operand)
                    new_stack.append(operator)
                elif operator == "+":
                    r_operand = stack.popleft()
                    result = operators[operator](l_operand, r_operand)
                    stack.appendleft(result)
                else:
                    raise Exception

        return reduce_stack_same_precedence_mode(new_stack)

    modes = {
        "same_precedence": reduce_stack_same_precedence_mode,
        "addition_first": reduce_stack_addition_first_mode,
    }

    def _calculate(parsed):
        stack = collections.deque()

        for element in parsed:
            if isinstance(element, list):
                item = _calculate(element)
            else:
                item = element
            stack.append(item)

        resultant_stack = modes[mode](stack)
        return resultant_stack.pop()

    return _calculate(parsed)


def process(input_str, mode):
    parsed = parse(input_str)
    result = calculate(parsed, mode)
    return result


def read_file():
    with open("input.txt") as f:
        return f.read().splitlines()


def main():
    input_str = read_file()
    processed_same_precedence = [
        process(line, mode="same_precedence") for line in input_str
    ]
    print(
        f"Sum of resulting values in same precedence mode: {sum(processed_same_precedence)}"
    )
    processed_addition_first = [
        process(line, mode="addition_first") for line in input_str
    ]
    print(
        f"Sum of resulting values in addition first mode: {sum(processed_addition_first)}"
    )


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
