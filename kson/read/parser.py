from . import hooks
from .json_transformer import JsonTransformer
from pathlib import Path
import functools
import lark

GRAMMAR_DIR = Path(__file__).parents[2] / 'grammar'
JSON_GRAMMAR = (GRAMMAR_DIR / 'json.lark').read_text()
KSON_GRAMMAR = (GRAMMAR_DIR / 'kson.lark').read_text()
JSON_TRANSFORMER = JsonTransformer()
KSON_TRANSFORMER = hooks.HOOKS._transformer()


def _lark(transformer=KSON_TRANSFORMER, use_bytes=False, grammar=KSON_GRAMMAR):
    return lark.Lark(
        grammar,
        transformer=transformer,
        parser='lalr',
        lexer='standard',
        propagate_positions=False,
        maybe_placeholders=False,
        use_bytes=use_bytes,
    )


def _names():
    found = set()
    for rule in _lark(KSON_TRANSFORMER).rules:
        name = rule.origin.name
        if name not in found:
            yield name
            found.add(name)


NAMES = _names()


def _parser(transformer, use_bytes=False, grammar=KSON_GRAMMAR):
    return _lark(transformer, use_bytes, grammar).parser.parse


@functools.lru_cache()
def parser(transformer=KSON_TRANSFORMER, use_bytes=False):
    return _parser(transformer, use_bytes)


parse_string = parser()
parse_bytes = parser(use_bytes=True)


# Legacy - for comparison testing only
parse_json = _parser(JSON_TRANSFORMER, grammar=JSON_GRAMMAR)


def parse(s):
    if isinstance(s, str):
        return parse_string(s)
    return parse_bytes(s)
