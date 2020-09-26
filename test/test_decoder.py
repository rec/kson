from kson.read import decoder
import unittest


def make_decoder(s):
    d = decoder.Decoder()
    calls = []

    def wrap(name):
        orig = getattr(d, name)

        def wrapped(*args, **kwargs):
            calls.append((name, args, kwargs))
            return orig(*args, **kwargs)

        return wrapped

    for name in decoder.NAMES:
        setattr(d, name, wrap(name))

    return d(s), calls


class DecoderTest(unittest.TestCase):
    def test_empty(self):
        result, calls = make_decoder('""')
        assert result == ''
        assert calls == [('string', ('""',), {})]
