from . import quotes

SHORT_ASCII = '\\u{0:04x}'
LONG_ASCII = '\\u{0:04x}\\u{1:04x}'


def quoter(double_quote: bool = False, ensure_ascii: bool = False):
    q = quotes.QUOTES[double_quote]

    def quote(s):
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

    return quote
