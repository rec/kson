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
    @inline
    def array(self, *args):
        return list(args)

    @inline
    def object(self, *args):
        return dict(args)

    @inline
    def key_value(self, k, v):
        return k, v

    @inline
    def integer(self, i):
        return int(i)

    @inline
    def floating(self, i):
        return float(i)

    @inline
    def null(self):
        return None

    @inline
    def false(self):
        return False

    @inline
    def true(self):
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

    @inline
    def nan(self):
        return math.nan

    @inline
    def inf(self):
        return math.inf

    @inline
    def minus_inf(self):
        return -math.inf
