from argparse import Namespace
from json import decoder, encoder
import functools
import re

compile_re = functools.partial(re.compile, flags=decoder.FLAGS)

SINGLE = "'"
DOUBLE = '"'


def quotes(s: str):
    assert isinstance(s, str)
    return QUOTES[s[0] == DOUBLE]


def _single():
    for k, v in vars(DOUBLE_QUOTES).items():
        if isinstance(v, str):
            v = v.replace(DOUBLE, SINGLE)

        elif hasattr(v, 'pattern'):
            v = compile_re(v.pattern.replace(DOUBLE, SINGLE))

        else:
            assert isinstance(v, dict)
            v = dict(v)
            v.pop(DOUBLE)
            if k == 'escape_dict':
                v[SINGLE] = '\\' + SINGLE
            else:
                assert k == 'backslash_dict'
                v[SINGLE] = SINGLE

        yield k, v


DOUBLE_QUOTES = Namespace(
    quote=DOUBLE,
    # read
    string_chunk_re=decoder.STRINGCHUNK,
    backslash_dict=decoder.BACKSLASH,
    # write
    escape_re=encoder.ESCAPE,
    escape_ascii_re=encoder.ESCAPE_ASCII,
    escape_dict=encoder.ESCAPE_DCT,
)

SINGLE_QUOTES = Namespace(**dict(_single()))
QUOTES = SINGLE_QUOTES, DOUBLE_QUOTES
