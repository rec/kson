from .grammar import json, kson
from .transformer import JsonTransformer, KsonTransformer
from pathlib import Path
import lark

UUID = '3b69df96-a44b-460b-9542-eaf9dd2a98a8'
STANDALONE = False


def make_lark(file, is_kson=False, **kwargs):
    transformer = KsonTransformer() if is_kson else JsonTransformer()

    if STANDALONE and is_kson:
        Lark = kson.Lark_StandAlone if is_kson else json.Lark_StandAlone
        return Lark(file)

    return lark.Lark(
        Path(file).read_text(),
        transformer=transformer,
        parser='lalr',
        lexer='standard',
        propagate_positions=False,
        maybe_placeholders=False,
        **kwargs
    )


def make_parser(file, is_kson=False, **kwargs):
    return make_lark(file, is_kson, **kwargs).parse
