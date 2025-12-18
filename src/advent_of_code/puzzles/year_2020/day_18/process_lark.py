import functools
import timeit
from typing import cast

import lark


calc_grammar_template = """
    ?start: expr
    {order_of_operations}
    ?atom: NUMBER           -> number
         | "(" expr ")"
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

traditional_calc_grammar = calc_grammar_template.format(
    order_of_operations="""
    ?expr: sum
    ?sum: product
        | sum "+" product   -> add
    ?product: atom
        | product "*" atom  -> mul
"""
)

same_precedence_calc_grammar = calc_grammar_template.format(
    order_of_operations="""
    ?expr: atom
        | expr "+" atom  -> add
        | expr "*" atom  -> mul
"""
)

add_first_calc_grammar = calc_grammar_template.format(
    order_of_operations="""
    ?expr: product
    ?product: sum
        | product "*" sum  -> mul    
    ?sum: atom
        | sum "+" atom     -> add
"""
)


@lark.v_args(inline=True)
class CalculateTree(lark.Transformer):
    from operator import add, mul

    number = int


lark_parser_partial = functools.partial(
    lark.Lark, parser="lalr", transformer=CalculateTree()
)

traditional_calc_parser = lark_parser_partial(traditional_calc_grammar)
traditional_calc = traditional_calc_parser.parse

same_precedence_calc_parser = lark_parser_partial(same_precedence_calc_grammar)
same_precedence_calc = same_precedence_calc_parser.parse

add_first_calc_parser = lark_parser_partial(add_first_calc_grammar)
add_first_calc = add_first_calc_parser.parse


class OperationOrder:
    def __init__(self, expressions):
        self.expressions = expressions

    @classmethod
    def read_file(cls):
        expressions = []
        with open("input.txt") as f:
            for raw_line in f:
                line = raw_line.rstrip()
                expressions.append(line)
        return cls(expressions)

    @property
    def result_same_precedence(self):
        total = 0
        for expression in self.expressions:
            result = same_precedence_calc(expression)
            result = cast(int, result)
            total += result
        return total

    @property
    def result_addition_first(self):
        total = 0
        for expression in self.expressions:
            result = add_first_calc(expression)
            result = cast(int, result)
            total += result
        return total


def main():
    operation_order = OperationOrder.read_file()
    print("Same precedence:", operation_order.result_same_precedence)
    print("Addition first:", operation_order.result_addition_first)


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
