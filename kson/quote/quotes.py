from argparse import Namespace
from json import decoder, encoder
import functools
import re

compile_re = functools.partial(re.compile, flags=decoder.FLAGS)

SINGLE = "'"
DOUBLE = '"'


def quotes(s: str):
    assert isinstance(s, str)
    double_quote = s[0] == DOUBLE
    return get_quotes(double_quote)


def get_quotes(double_quote: bool = False):
    return QUOTES[double_quote]


def _single():
    for k, v in vars(DOUBLE_QUOTES).items():
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
                v[SINGLE] = '\\' + SINGLE
            else:
                assert k == 'backslash_dict'
                v[SINGLE] = SINGLE
        else:
            raise TypeError(f'{v=}, {type(v)=}')

        yield k, v


DOUBLE_QUOTES = Namespace(
    quote=DOUBLE,

    # read
    string_chunk_re=decoder.STRINGCHUNK,
    backslash_dict=decoder.BACKSLASH,
    unicode_marker='u',

    # write
    escape_re=encoder.ESCAPE,
    escape_ascii_re=encoder.ESCAPE_ASCII,
    escape_dict=encoder.ESCAPE_DCT,
    short_ascii='\\u{0:04x}',
    long_ascii='\\u{0:04x}\\u{1:04x}',
)

SINGLE_QUOTES = Namespace(**dict(_single()))
QUOTES = SINGLE_QUOTES, DOUBLE_QUOTES
