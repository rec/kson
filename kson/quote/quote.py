from . import tables
from argparse import Namespace
import functools

SHORT_ASCII = '\\u{0:04x}'
LONG_ASCII = '\\u{0:04x}\\u{1:04x}'


def quotes(s):
    assert isinstance(s, str)
    return QUOTES[s[0] == tables.SINGLE]


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


QUOTES = tuple(Namespace(**t) for t in tables.QUOTES)
