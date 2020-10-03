from .. grammar import kson
from .. import quote
import base64
import functools
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
        tr = self._transformer()
        if not use_bytes:
            return kson.Lark_StandAlone(tr)

        return kson.Lark._load_from_dict(BINARY, kson.MEMO, transformer=tr)

    @functools.lru_cache()
    def _transformer(self):
        t = kson.Transformer()
        t.__dict__.update({k: _wrap(self, k) for k in NAMES})
        return t

    def __call__(self, s):
        return self._lark(_is_bytes(s)).parser.parse(s)


def _wrap(obj, name):
    method = getattr(obj, name)
    encode = (lambda x: x) if name.endswith('bytes') else quote.encode

    @functools.wraps(method)
    def wrapped(x):
        return method(*[encode(getattr(i, 'value', i)) for i in x])

    return wrapped


def _is_bytes(s):
    if isinstance(s, (bytes, bytearray)):
        return True
    if not isinstance(s, str):
        raise TypeError('Must be bytes, bytearray or str')


def _use_bytes(d):
    if isinstance(d, list):
        return [_use_bytes(i) for i in d]
    if isinstance(d, dict):
        r = {}
        for k, v in d.items():
            r[k] = k == 'use_bytes' or _use_bytes(v)
        return r
    return d


BINARY = _use_bytes(kson.DATA)
NAMES = [i for i in Decoder.__dict__ if not i.startswith('_')]
DECODER = Decoder()
