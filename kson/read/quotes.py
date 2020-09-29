from .to_bytes import to_bytes, compile_re
from dataclasses import dataclass, field
from json import decoder, encoder
import re

SINGLE = "'"
DOUBLE = '"'


def quotes(s):
    use_bytes = not isinstance(s, str)
    is_single_quote = s[0] in {SINGLE, SINGLE.encode()}
    return QUOTES[is_single_quote][use_bytes]


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


def to_single(quote):
    u = Quotes()
    for k in quote.__dataclass_fields__:
        v = getattr(quote, k)
        if isinstance(v, str):
            v = v.replace(DOUBLE, SINGLE)
        elif isinstance(v, re.Pattern):
            v = compile_re(v.pattern.replace(DOUBLE, SINGLE))
        elif isinstance(v, dict):
            v = dict(v)
            v.pop(DOUBLE)
            v[SINGLE] = SINGLE
        else:
            raise TypeError
        setattr(u, k, v)
    return u


DOUBLE_QUOTES = Quotes()
SINGLE_QUOTES = to_single(DOUBLE_QUOTES)

QUOTES = (
    (DOUBLE_QUOTES, to_bytes(DOUBLE_QUOTES)),
    (SINGLE_QUOTES, to_bytes(SINGLE_QUOTES)),
)
