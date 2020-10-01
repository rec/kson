from . import parser
from ..quote import unquote
import base64
import functools
import lark
import math


class Decoder:
    _ENFORCE_STRINGS = False

    def start(self, *args):
        return args

    def value(self, x):
        return x

    def object(self, *args):
        return dict(args)

    def key_value(self, k, v):
        return k, v

    def array(self, *args):
        return list(args)

    def string(self, s):
        return unquote.unquote(s)

    def abytes(self, s):
        return base64.b85decode(s[2:-1])

    def bbytes(self, s):
        tsize = 1 + s.index(s[1], 2)
        assert s.endswith(s[1:tsize])
        return s[tsize : -tsize + 1]

    def integer(self, i):
        return int(i)

    def floating(self, i):
        return float(i)

    def false(self):
        return False

    def true(self):
        return True

    def null(self):
        return None

    def nan(self):
        return math.nan

    def inf(self):
        return math.inf

    def minus_inf(self):
        return -math.inf

    @functools.lru_cache()
    def _lark(self, use_bytes):
        return parser.lark(self._transformer(), use_bytes)

    @functools.lru_cache()
    def _transformer(self):
        t = lark.Transformer()
        for name in NAMES:
            setattr(t, name, _wrap(getattr(self, name)))

        return t

    def __call__(self, s):
        return self._lark(_use_bytes(s)).parser.parse(s)


def _wrap(method):
    @functools.wraps(method)
    def wrapped(x):
        x = (getattr(i, 'value', i) for i in x)
        if Decoder._ENFORCE_STRINGS:
            x = [i if isinstance(i, str) else i.encode() for i in x]
        return method(*x)

    return wrapped


def _use_bytes(s):
    if isinstance(s, (bytes, bytearray)):
        return True
    if not isinstance(s, str):
        raise TypeError('Must be bytes, bytearray or str')


NAMES = [i for i in Decoder.__dict__ if not i.startswith('_')]
DECODER = Decoder()
