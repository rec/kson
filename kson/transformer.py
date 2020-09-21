import base64
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
        s = regex.sub(r'\1' + s[0], s[1:-1])
        return RETURN_RE.sub(r'\1', s)

    def astring(self, s):
        s = s[0]
        assert len(s) >= 3, '%s, %s' % (len(s), s)
        assert s[0] == 'a'
        assert s[1] in '"\''
        assert s[-1] == s[1]
        return base64.b85decode(s[2:-1])

    def bstring(self, s):
        s = s[0].value
        if False:
            for k in dir(s):
                if not k.startswith('_'):
                    print('-', k, getattr(s, k))
        tsize = s.index(b'>')
        if not s.endswith(b'</' + s[:tsize]):
            raise ValueError('A bstring must end with its token')
        return s[tsize + 1 : -tsize - 2]
