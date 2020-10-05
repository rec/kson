from .. grammar import kson
from .. quote import quote as _quote
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
        return _quote.unquote(s)

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
        if _is_bin(s):
            lark = self._lark(True)
        elif not isinstance(s, str):
            raise TypeError('Must be bytes, bytearray or str')
        else:
            lark = self._lark(False)

        return lark.parser.parse(s)


def _wrap(obj, name):
    method = getattr(obj, name)

    def encode(s):
        return s.decode() if _is_bin(s) else s

    enc = (lambda x: x) if name.endswith('bytes') else encode

    @functools.wraps(method)
    def wrapped(x):
        return method(*[enc(getattr(i, 'value', i)) for i in x])

    return wrapped


def _use_bytes(d):
    if isinstance(d, list):
        return [_use_bytes(i) for i in d]
    if isinstance(d, dict):
        r = {}
        for k, v in d.items():
            r[k] = k == 'use_bytes' or _use_bytes(v)
        return r
    return d


def _is_bin(s):
    return isinstance(s, (bytearray, bytes))


BINARY = _use_bytes(kson.DATA)
NAMES = [i for i in Decoder.__dict__ if not i.startswith('_')]
DECODER = Decoder()
