from . import quote
from . import quotes
from .unquote import unquote

assert quote and quotes and unquote
ENFORCE_STRINGS = True

if ENFORCE_STRINGS:

    def encode(s):
        return s.decode() if isinstance(s, bytes) else s


else:

    def encode(s):
        return s
