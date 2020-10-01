from . import quote
from . import quotes
from .unquote import unquote

assert quote and quotes and unquote


def encode(s):
    return s.decode() if isinstance(s, bytes) else s
