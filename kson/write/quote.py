from ..read import quotes
import functools


def quoter(double_quote: bool = False, ensure_ascii: bool = False):
    return functools.partial(
        quote_ascii if ensure_ascii else quote_unicode,
        quotes.get_quotes(double_quote),
    )


def quote_unicode(quotes, s):
    """
    Return a KSON representation of a Python string with
    single quotes, allowing arbitary Unicode characters
    """
    print('quote_unicode', quotes.escape_dict)

    def replace(match):
        return quotes.escape_dict[match.group(0)]

    return quotes.quote + quotes.escape_re.sub(replace, s) + quotes.quote


def quote_ascii(quotes, s):
    """
    Return an ASCII-only KSON representation of a Python string with
    single quotes
    """

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
