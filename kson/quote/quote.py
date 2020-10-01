from . import quotes


def quoter(double_quote: bool = False, ensure_ascii: bool = False):
    q = quotes.get_quotes(double_quote)

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
                return q.short_ascii.format(n)

            # surrogate pair
            n -= 0x10000
            s1 = 0xD800 | ((n >> 10) & 0x3FF)
            s2 = 0xDC00 | (n & 0x3FF)
            return q.long_ascii.format(s1, s2)

        if ensure_ascii:
            sub = q.escape_ascii_re.sub(replace_ascii, s)
        else:
            sub = q.escape_re.sub(replace_unicode, s)

        return q.quote + sub + q.quote

    return quote
