from .json_transformer import JsonTransformer
from .transformer import KsonTransformer
from pathlib import Path
import lark


def _parser(grammar, transformer, use_bytes):
    return lark.Lark(
        grammar,
        transformer=transformer,
        parser='lalr',
        lexer='standard',
        propagate_positions=False,
        maybe_placeholders=False,
        use_bytes=use_bytes,
    ).parser.parse


GRAMMAR_DIR = Path(__file__).parents[1] / 'grammar'
JSON_GRAMMAR = (GRAMMAR_DIR / 'json.lark').read_text()
KSON_GRAMMAR = (GRAMMAR_DIR / 'kson.lark').read_text()

parse_json = _parser(JSON_GRAMMAR, JsonTransformer(), False)
parse_string = _parser(KSON_GRAMMAR, KsonTransformer(), False)
parse_bytes = _parser(KSON_GRAMMAR, KsonTransformer(), True)


def parse(s):
    if isinstance(s, str):
        return parse_string(s)
    return parse_bytes(s)
