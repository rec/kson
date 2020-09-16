from pathlib import Path
import lark


def make_lark(file, transformer):
    return lark.Lark(
        Path(file).read_text(),
        transformer=transformer,
        parser='lalr',
        lexer='standard',
        propagate_positions=False,
        maybe_placeholders=False,
    )


def make_parser(file, transformer):
    return make_lark(file, transformer).parse
