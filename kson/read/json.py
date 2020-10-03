from . import parser
import lark
import re

DOUBLE_QUOTE_RE = re.compile(r'(?<!\\)(\\\\)*\\(")')
JSON_GRAMMAR = parser.grammar('json')


class JsonTransformer(lark.Transformer):
    def string(self, s):
        s = s[0]
        return DOUBLE_QUOTE_RE.sub(r'\1' + s[0], s[1:-1])

    array = list
    object = dict
    object_entry = tuple

    def integer(self, s):
        return int(s[0])

    def floating(self, s):
        return float(s[0])

    def null(self, _):
        return None

    def false(self, _):
        return False

    def true(self, _):
        return True


parse = parser.parser(JsonTransformer(), grammar=JSON_GRAMMAR)
