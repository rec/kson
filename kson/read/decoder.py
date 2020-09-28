from . import parser
from . import unquote
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
        return unquote.unquote(s)

    def astring(self, s):
        return base64.b85decode(s[2:-1])

    def bstring(self, s):
        v = s.value
        tsize = 1 + v.index(v[1], 2)
        assert v.endswith(v[1:tsize])
        return v[tsize : -tsize + 1]

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
        def wrap(name):
            attr = getattr(self, name)
            return lambda x: attr(*x)

        t = lark.Transformer()
        t.__dict__.update((name, wrap(name)) for name in NAMES)
        return t

    def __call__(self, s):
        if isinstance(s, str):
            use_bytes = False
        elif isinstance(s, (bytes, bytearray)):
            use_bytes = True
        else:
            raise TypeError('Must be bytes, bytearray or str')

        return self._lark(use_bytes).parser.parse(s)


NAMES = [i for i in Decoder.__dict__ if not i.startswith('_')]
DECODER = Decoder()
