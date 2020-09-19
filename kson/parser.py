from pathlib import Path
import lark
from . transformer import JsonTransformer, KsonTransformer

UUID = '3b69df96-a44b-460b-9542-eaf9dd2a98a8'


def make_lark(file, is_kson=False):
    transformer = KsonTransformer() if is_kson else JsonTransformer()
    return lark.Lark(
        Path(file).read_text(),
        transformer=transformer,
        parser='lalr',
        lexer='standard',
        propagate_positions=False,
        maybe_placeholders=False,
    )


def make_parser(file, is_kson=False):
    return make_lark(file, is_kson).parse
