from .to_bytes import to_bytes, compile_re
from dataclasses import dataclass, field
from json import decoder, encoder
import re

SINGLE = "'"
DOUBLE = '"'


def quotes(s: str):
    use_bytes = not isinstance(s, str)
    double_quote = s[:1] in {DOUBLE, DOUBLE.encode()}
    return get_quotes(double_quote, use_bytes)


def get_quotes(double_quote: bool = False, use_bytes: bool = False):
    return QUOTES[double_quote][use_bytes]


@dataclass
class Quotes:
    quote: object = DOUBLE
    backslash: object = "\\"

    # read
    string_chunk_re: re.Pattern = decoder.STRINGCHUNK
    backslash_dict: dict = field(default_factory=decoder.BACKSLASH.copy)
    unicode_marker: object = 'u'

    # write
    escape_re: re.Pattern = encoder.ESCAPE
    escape_ascii_re: re.Pattern = encoder.ESCAPE_ASCII
    escape_dict: dict = field(default_factory=encoder.ESCAPE_DCT.copy)
    short_ascii: object = '\\u{0:04x}'
    long_ascii: object = '\\u{0:04x}\\u{1:04x}'


def to_single(quote):
    q = {}
    for k, v in vars(quote).items():
        if k.startswith('_'):
            continue

        if isinstance(v, str):
            v = v.replace(DOUBLE, SINGLE)

        elif isinstance(v, re.Pattern):
            v = compile_re(v.pattern.replace(DOUBLE, SINGLE))

        elif isinstance(v, dict):
            v = dict(v)
            v.pop(DOUBLE)
            if k == 'escape_dict':
                v[SINGLE] = quote.backslash + SINGLE
            else:
                assert k == 'backslash_dict'
                v[SINGLE] = SINGLE
        else:
            raise TypeError

        q[k] = v

    return Quotes(**q)


DOUBLE_QUOTES = Quotes()
SINGLE_QUOTES = to_single(DOUBLE_QUOTES)

QUOTES = (
    (SINGLE_QUOTES, to_bytes(SINGLE_QUOTES)),
    (DOUBLE_QUOTES, to_bytes(DOUBLE_QUOTES)),
)
