import lark
import sys


def make_parser(module):
    return lark.Lark(
        module.GRAMMAR,
        transformer=module.Transformer(),
        parser='lalr',
        lexer='standard',
        propagate_positions=False,
        maybe_placeholders=False,
    ).parse


if __name__ == '__main__':
    import json_parser

    parse = make_parser(json_parser)

    with open(sys.argv[1]) as f:
        print(parse(f.read()))
