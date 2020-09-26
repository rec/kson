from . import get_lark
from . import hooks
from . import json
import functools

KSON_TRANSFORMER = hooks.HOOKS._transformer()


def _names():
    found = set()
    for rule in get_lark(KSON_TRANSFORMER).rules:
        name = rule.origin.name
        if name not in found:
            yield name
            found.add(name)


NAMES = _names()


def _parser(transformer, use_bytes=False, grammar=get_lark.KSON_GRAMMAR):
    return get_lark.get_lark(transformer, use_bytes, grammar).parser.parse


@functools.lru_cache()
def parser(transformer=KSON_TRANSFORMER, use_bytes=False):
    return _parser(transformer, use_bytes)


parse_string = parser()
parse_bytes = parser(use_bytes=True)


# Legacy - for comparison testing only
parse_json = _parser(json.TRANSFORMER, grammar=get_lark.JSON_GRAMMAR)


def parse(s):
    if isinstance(s, str):
        return parse_string(s)
    return parse_bytes(s)
