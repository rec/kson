from argparse import Namespace
from json import decoder, encoder
import functools
import re

SHORT_ASCII = '\\u{0:04x}'
LONG_ASCII = '\\u{0:04x}\\u{1:04x}'

compile_re = functools.partial(re.compile, flags=decoder.FLAGS)

SINGLE = "'"
DOUBLE = '"'


def quotes(s: str):
    assert isinstance(s, str)
    return QUOTES[s[0] == SINGLE]


def _single():
    for k, v in vars(DOUBLE_QUOTES).items():
        if isinstance(v, str):
            v = v.replace(DOUBLE, SINGLE)

        elif hasattr(v, 'pattern'):
            v = compile_re(v.pattern.replace(DOUBLE, SINGLE))

        else:
            assert isinstance(v, dict)
            v = dict(v)
            v.pop(DOUBLE)
            if k == 'escape_dict':
                v[SINGLE] = '\\' + SINGLE
            else:
                assert k == 'backslash_dict'
                v[SINGLE] = SINGLE

        yield k, v


DOUBLE_QUOTES = Namespace(
    quote=DOUBLE,
    # read
    string_chunk_re=decoder.STRINGCHUNK,
    backslash_dict=decoder.BACKSLASH,
    # write
    escape_re=encoder.ESCAPE,
    escape_ascii_re=encoder.ESCAPE_ASCII,
    escape_dict=encoder.ESCAPE_DCT,
)


def quoter(single_quote=False, ensure_ascii=False):
    q = QUOTES[single_quote]
    return functools.partial(quote, q, ensure_ascii=ensure_ascii)


def quote(q, s, ensure_ascii=False):
    def replace_unicode(match):
        return q.escape_dict[match.group(0)]

    def replace_ascii(match):
        s = match.group(0)
        try:
            return q.escape_dict[s]
        except KeyError:
            pass

        n = ord(s) if isinstance(s, str) else s
        if n < 0x10000:
            return SHORT_ASCII.format(n)

        # surrogate pair
        n -= 0x10000
        s1 = 0xD800 | ((n >> 10) & 0x3FF)
        s2 = 0xDC00 | (n & 0x3FF)
        return LONG_ASCII.format(s1, s2)

    if ensure_ascii:
        re, replace = q.escape_ascii_re, replace_ascii
    else:
        re, replace = q.escape_re, replace_unicode

    return q.quote + re.sub(replace, s) + q.quote


SINGLE_QUOTES = Namespace(**dict(_single()))
QUOTES = DOUBLE_QUOTES, SINGLE_QUOTES
