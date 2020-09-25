from .transformer import ODD_BACKSLASHES
from .transformer import inline
import lark
import re

DOUBLE_QUOTE_RE = re.compile(ODD_BACKSLASHES + '(")')


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
