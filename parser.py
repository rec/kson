from pathlib import Path
import lark
import transformer


def make_parser(file):
    return lark.Lark(
        Path(file).read_text(),
        transformer=transformer.Transformer(),
        parser='lalr',
        lexer='standard',
        propagate_positions=False,
        maybe_placeholders=False,
    ).parse
