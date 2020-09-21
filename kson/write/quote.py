from json import encoder
import re

ESCAPE = re.compile(encoder.ESCAPE.pattern.replace('"', "'"))
ESCAPE_ASCII = re.compile(encoder.ESCAPE_ASCII.pattern.replace('"', "'"))
ESCAPE_DCT = dict(encoder.ESCAPE_DCT)
del ESCAPE_DCT['"']
ESCAPE_DCT["'"] = "\\'"


def quoter(double_quote: bool, ensure_ascii: bool):
    if double_quote:
        return double_ascii if ensure_ascii else double
    return single_ascii if ensure_ascii else single


double = encoder.encode_basestring
double_ascii = encoder.encode_basestring_ascii


def single(s):
    def replace(match):
        return ESCAPE_DCT[match.group(0)]

    return "'" + ESCAPE.sub(replace, s) + "'"


def single_ascii(s):
    """Return an ASCII-only KSON representation of a Python string
    """
    def replace(match):
        s = match.group(0)
        try:
            return ESCAPE_DCT[s]
        except KeyError:
            n = ord(s)
            if n < 0x10000:
                return '\\u{0:04x}'.format(n)
            else:
                # surrogate pair
                n -= 0x10000
                s1 = 0xd800 | ((n >> 10) & 0x3ff)
                s2 = 0xdc00 | (n & 0x3ff)
                return '\\u{0:04x}\\u{1:04x}'.format(s1, s2)

    return "'" + ESCAPE_ASCII.sub(replace, s) + "'"
