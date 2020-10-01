from . import quotes


def quoter(double_quote: bool = False, ensure_ascii: bool = False):
    do_quote = quote_ascii if ensure_ascii else quote_unicode

    def quote(s):
        assert isinstance(s, str)
        quote = quotes.get_quotes(double_quote)
        return do_quote(quote, s)

    return quote


def quote_unicode(quotes, s):
    def replace(match):
        return quotes.escape_dict[match.group(0)]

    return quotes.quote + quotes.escape_re.sub(replace, s) + quotes.quote


def quote_ascii(quotes, s):
    def replace(match):
        s = match.group(0)
        try:
            return quotes.escape_dict[s]
        except KeyError:
            n = ord(s) if isinstance(s, str) else s

            if n < 0x10000:
                return quotes.short_ascii.format(n)
            else:
                # surrogate pair
                n -= 0x10000
                s1 = 0xD800 | ((n >> 10) & 0x3FF)
                s2 = 0xDC00 | (n & 0x3FF)
                return quotes.long_ascii.format(s1, s2)

    return quotes.quote + quotes.escape_ascii_re.sub(replace, s) + quotes.quote
