import base64
import lark
import re
from .write import unquote
import math

inline = lark.v_args(inline=True)

ODD_BACKSLASHES = r'(?<!\\)(\\\\)*\\'
RETURN_RE = re.compile(ODD_BACKSLASHES + '\n')
QUOTE_RE = re.compile(ODD_BACKSLASHES + "(')")
DOUBLE_QUOTE_RE = re.compile(ODD_BACKSLASHES + '(")')


class JsonTransformer(lark.Transformer):
    @inline
    def string(self, s):
        return DOUBLE_QUOTE_RE.sub(r'\1' + s[0], s[1:-1])

    array = list
    pair = tuple
    object = dict
    number = inline(float)

    def null(self, _):
        return None

    def false(self, _):
        return False

    def true(self, _):
        return True


class KsonTransformer(JsonTransformer):
    @inline
    def string(self, s):
        return unquote.unquote(s)

    @inline
    def astring(self, s):
        return base64.b85decode(s[2:-1])

    @inline
    def bstring(self, s):
        s = s.value
        tsize = s.index(b'>')
        if not s.endswith(b'</' + s[:tsize]):
            raise ValueError('A bstring must end with its token')
        return s[tsize + 1 : -tsize - 2]

    def nan(self, _):
        return math.nan

    def inf(self, _):
        return math.inf

    def minus_inf(self, _):
        return -math.inf
