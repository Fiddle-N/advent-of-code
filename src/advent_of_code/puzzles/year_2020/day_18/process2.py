import collections
import operator
import string
import timeit


class OperationOrder:
    def __init__(self, expressions):
        self.expressions = expressions

    @classmethod
    def read_file(cls):
        expressions = []
        with open("input.txt") as f:
            for raw_line in f:
                line = raw_line.rstrip()
                expressions.append(MathExpression.parse(line))
        return cls(expressions)

    @property
    def result_same_precedence(self):
        return sum(expression.result_same_precedence for expression in self.expressions)

    @property
    def result_addition_first(self):
        return sum(expression.result_addition_first for expression in self.expressions)


class MathExpression:
    OPERATORS = {
        "+": operator.add,
        "*": operator.mul,
    }

    def __init__(self, expression):
        self.expression = expression

    @classmethod
    def parse(cls, raw_expr):
        inst, _ = cls._parse(raw_expr)
        return inst

    @classmethod
    def _parse(cls, raw_expr):
        raw_expr = iter(raw_expr)
        items = []
        for item in raw_expr:
            if item == "(":
                result, closeparen = cls._parse(raw_expr)
                if not closeparen:
                    raise ValueError("bad expression -- unbalanced parentheses")
                items.append(result)
            elif item == ")":
                return MathExpression(items), True
            elif item in string.whitespace:
                continue
            else:
                try:
                    item = int(item)
                except ValueError:
                    if item not in ("+", "*"):
                        raise
                items.append(item)
        return MathExpression(items), False

    def __repr__(self):
        return f"MthExpr({self.expression})"

    @property
    def result_same_precedence(self):
        stack = collections.deque(self.expression)
        return self._result_same_precedence(stack)

    def _result_same_precedence(self, stack):
        while len(stack) > 1:
            raw_l_operand = stack.popleft()
            operation = stack.popleft()
            raw_r_operand = stack.popleft()
            l_operand = self.get_operand_result(
                raw_l_operand, result_type="result_same_precedence"
            )
            r_operand = self.get_operand_result(
                raw_r_operand, result_type="result_same_precedence"
            )
            result = self.OPERATORS[operation](l_operand, r_operand)
            stack.appendleft(result)
        return stack[0]

    def get_operand_result(self, operand, result_type):
        return (
            getattr(operand, result_type)
            if isinstance(operand, MathExpression)
            else operand
        )

    @property
    def result_addition_first(self):
        stack = collections.deque(self.expression)
        new_stack = collections.deque()

        while stack:
            raw_l_operand = stack.popleft()
            l_operand = self.get_operand_result(
                raw_l_operand, result_type="result_addition_first"
            )
            try:
                operator = stack.popleft()
            except IndexError:  # only one element in the original stack
                new_stack.append(l_operand)
            else:
                if operator == "*":
                    new_stack.append(l_operand)
                    new_stack.append(operator)
                elif operator == "+":
                    raw_r_operand = stack.popleft()
                    r_operand = self.get_operand_result(
                        raw_r_operand, result_type="result_addition_first"
                    )
                    result = self.OPERATORS[operator](l_operand, r_operand)
                    stack.appendleft(result)
                else:
                    raise Exception

        return self._result_same_precedence(new_stack)


def main():
    operation_order = OperationOrder.read_file()
    print("Same precedence:", operation_order.result_same_precedence)
    print("Addition first:", operation_order.result_addition_first)


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
