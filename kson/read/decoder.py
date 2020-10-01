from . import parser
from .. import quote
import base64
import functools
import lark
import math


class Decoder:
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
        return quote.unquote(s)

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
        t.__dict__.update({k: _wrap(self, k) for k in NAMES})
        return t

    def __call__(self, s):
        return self._lark(_use_bytes(s)).parser.parse(s)


def _wrap(obj, name):
    method = getattr(obj, name)
    encode = (lambda x: x) if name.endswith('bytes') else quote.encode

    @functools.wraps(method)
    def wrapped(x):
        return method(*[encode(getattr(i, 'value', i)) for i in x])

    return wrapped


def _use_bytes(s):
    if isinstance(s, (bytes, bytearray)):
        return True
    if not isinstance(s, str):
        raise TypeError('Must be bytes, bytearray or str')


NAMES = [i for i in Decoder.__dict__ if not i.startswith('_')]
DECODER = Decoder()
