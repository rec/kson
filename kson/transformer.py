from .write import unquote
import base64
import lark
import math
import re

inline = lark.v_args(inline=True)

ODD_BACKSLASHES = r'(?<!\\)(\\\\)*\\'
RETURN_RE = re.compile(ODD_BACKSLASHES + '\n')
QUOTE_RE = re.compile(ODD_BACKSLASHES + "(')")


class KsonTransformer(lark.Transformer):
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

    @inline
    def string(self, s):
        return unquote.unquote(s)

    @inline
    def astring(self, s):
        return base64.b85decode(s[2:-1])

    @inline
    def bstring(self, s):
        v = s.value
        tsize = v.index(b'>')
        if not v.endswith(b'</' + v[:tsize]):
            raise ValueError('A bstring must end with its token')
        return v[tsize + 1 : -tsize - 2]

    def nan(self, _):
        return math.nan

    def inf(self, _):
        return math.inf

    def minus_inf(self, _):
        return -math.inf
