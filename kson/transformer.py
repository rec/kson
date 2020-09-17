import lark
import re

args = lark.v_args(inline=True)

ODD_BACKSLASHES = r'(?<!\\)(\\\\)*\\'
RETURN_RE = re.compile(ODD_BACKSLASHES + '\n')
QUOTE_RE = re.compile(ODD_BACKSLASHES + "(')")
DOUBLE_QUOTE_RE = re.compile(ODD_BACKSLASHES + '(")')


class JsonTransformer(lark.Transformer):
    @args
    def string(self, s):
        return DOUBLE_QUOTE_RE.sub(r'\1' + s[0], s[1:-1])

    array = list
    pair = tuple
    object = dict
    number = args(float)

    def null(self, _):
        return None

    def false(self, _):
        return False

    def true(self, _):
        return True


class KsonTransformer(JsonTransformer):
    @args
    def string(self, s):
        regex = QUOTE_RE if s[0] == "'" else DOUBLE_QUOTE_RE
        return regex.sub(r'\1' + s[0], s[1:-1])
