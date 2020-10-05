from json import decoder
from json import encoder
import functools
import re

compile_re = functools.partial(re.compile, flags=decoder.FLAGS)

SINGLE = "'"
DOUBLE = '"'


def _tables(**double):
    single = {}
    for k, v in double.items():
        if isinstance(v, str):
            single[k] = v.replace(DOUBLE, SINGLE)

        elif hasattr(v, 'pattern'):
            single[k] = compile_re(v.pattern.replace(DOUBLE, SINGLE))

        else:
            assert isinstance(v, dict)
            v = dict(v)
            v.pop(DOUBLE)
            if k == 'escape_dict':
                v[SINGLE] = '\\' + SINGLE
            else:
                assert k == 'backslash_dict'
                v[SINGLE] = SINGLE
            single[k] = v

    return double, single


QUOTES = _tables(
    quote=DOUBLE,
    string_chunk_re=decoder.STRINGCHUNK,  # read parameters
    backslash_dict=decoder.BACKSLASH,
    escape_re=encoder.ESCAPE,  # write parameters
    escape_ascii_re=encoder.ESCAPE_ASCII,
    escape_dict=encoder.ESCAPE_DCT,
)
