from . import get_lark
import lark
import re

inline = lark.v_args(inline=True)

ODD_BACKSLASHES = r'(?<!\\)(\\\\)*\\'
DOUBLE_QUOTE_RE = re.compile(ODD_BACKSLASHES + '(")')

JSON_GRAMMAR = get_lark.grammar('json')


class JsonTransformer(lark.Transformer):
    @inline
    def string(self, s):
        return DOUBLE_QUOTE_RE.sub(r'\1' + s[0], s[1:-1])

    array = list
    object = dict
    object_entry = tuple
    integer = inline(int)
    floating = inline(float)

    def null(self, _):
        return None

    def false(self, _):
        return False

    def true(self, _):
        return True


parse = get_lark.parser(JsonTransformer(), grammar=JSON_GRAMMAR)
