from . import quote
from . import quotes
from .unquote import unquote

assert quote and quotes and unquote
ENFORCE_STRINGS = False

if ENFORCE_STRINGS:

    def encode(s):
        return s if isinstance(s, str) else s.encode()


else:

    def encode(s):
        return s
