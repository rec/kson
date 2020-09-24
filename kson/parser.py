from .transformer import JsonTransformer, KsonTransformer
from pathlib import Path
import lark


def _parser(is_kson, binary):
    file = 'grammar/kson.lark' if is_kson else 'grammar/json.lark'
    transformer = KsonTransformer() if is_kson else JsonTransformer()

    return lark.Lark(
        Path(file).read_text(),
        transformer=transformer,
        parser='lalr',
        lexer='standard',
        propagate_positions=False,
        maybe_placeholders=False,
        use_bytes=binary,
    ).parser.parse


parse_json = _parser(False, False)
parse_string = _parser(True, False)
parse_binary = _parser(True, True)


def parse(s):
    if isinstance(s, str):
        return parse_string(s)
    return parse_binary(s)
