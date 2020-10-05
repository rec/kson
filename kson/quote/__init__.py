from . import quote  # noqa: F401


def is_bin(s):
    return isinstance(s, (bytearray, bytes))


def encode(s):
    return s.decode() if is_bin(s) else s
