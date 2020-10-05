from . import tables
from . unquote import unquote as _unquote

SHORT_ASCII = '\\u{0:04x}'
LONG_ASCII = '\\u{0:04x}\\u{1:04x}'


class _Quote:
    def __init__(self, table):
        for k, v in table.items():
            setattr(self, k, v)

    def add(self, s, ensure_ascii=False):
        if ensure_ascii:
            re, replace = self.escape_ascii_re, self._replace_ascii
        else:
            re, replace = self.escape_re, self._replace_unicode

        return self.quote + re.sub(replace, s) + self.quote

    def remove(self, s, strict=False):
        return _unquote(self, s, strict)

    def _replace_unicode(self, match):
        return self.escape_dict[match.group(0)]

    def _replace_ascii(self, match):
        s = match.group(0)
        try:
            return self.escape_dict[s]
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


def Quote(b):
    return _QUOTES[bool(b)]


def unquote(s, strict=True):
    return _QUOTES[s[0] == tables.SINGLE].remove(s, strict)


_QUOTES = tuple(_Quote(t) for t in tables.QUOTES)
