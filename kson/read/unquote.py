from dataclasses import dataclass, field
from json import decoder, JSONDecodeError
import copy
import functools
import re


def unquote(s, strict=False):
    use_bytes = not isinstance(s, str)
    is_single_quote = s[0] in {"'", b"'"}

    unquoter = UNQUOTERS[is_single_quote][use_bytes]
    return unquoter(s, strict)


@dataclass
class Unquoter:
    quote: object = '"'
    backslash: object = '\\'
    string_chunk_re: object = decoder.STRINGCHUNK
    backslash_dict: dict = field(default_factory=decoder.BACKSLASH.copy)
    unicode_marker: object = 'u'

    def to_single(self):
        u = copy.deepcopy(self)
        u.quote = "'"
        pat = self.string_chunk_re.pattern.replace(self.quote, u.quote)
        u.string_chunk_re = _compile(pat)
        del u.backslash_dict[self.quote]
        u.backslash_dict[u.quote] = u.quote
        return u

    def __call__(self, s, strict=False):
        s = getattr(s, 'value', s)
        chunks = []
        end = 1

        while end:
            end = self._unquote_once(s, chunks, strict, end)
        return self.quote[:0].join(chunks)

    def _unquote_once(self, s, chunks, strict, end):
        chunk = self.string_chunk_re.match(s, end)
        if not chunk:
            raise JSONDecodeError('Unterminated string', s)

        (content, term), end = chunk.groups(), chunk.end()
        # Content is zero or more unescaped string characters
        if content:
            chunks.append(content)
        # Term is the end of string, a literal control character,
        # or a backslash denoting that an escape sequence follows
        if term == self.quote:
            return
        if term != self.backslash:
            if strict:
                msg = "Invalid control character {0!r} at".format(term)
                raise JSONDecodeError(msg, s, end)
            chunks.append(term)
            return end
        try:
            esc = s[end]
        except IndexError:
            raise JSONDecodeError('Unterminated string', s) from None

        # If not a unicode escape sequence, must be in the lookup table
        if esc != self.unicode_marker:
            try:
                char = self.backslash_dict[esc]
            except KeyError:
                msg = "Invalid \\escape: {0!r}".format(esc)
                raise JSONDecodeError(msg, s, end) from None
            else:
                chunks.append(char)
                return end + 1

        uni = _decode_uXXXX(s, end)
        end += 5
        ucode = self.backslash + self.unicode_marker
        if 0xD800 <= uni <= 0xDBFF and s[end : end + 2] == ucode:
            uni2 = _decode_uXXXX(s, end + 1)
            if 0xDC00 <= uni2 <= 0xDFFF:
                uni = 0x10000 + (((uni - 0xD800) << 10) | (uni2 - 0xDC00))
                end += 6
        if isinstance(s, str):
            char = chr(uni)
        else:
            char = bytes([uni])
        chunks.append(char)
        return end


def to_bytes(x):
    if isinstance(x, str):
        return x.encode()
    if isinstance(x, list):
        return [to_bytes(i) for i in x]
    if isinstance(x, dict):
        return {to_bytes(k): to_bytes(v) for k, v in x.items()}
    if isinstance(x, re.Pattern):
        return _compile(to_bytes(x.pattern))

    df = getattr(x, '__dataclass_fields__', None)
    if df is not None:
        fields = {k: to_bytes(getattr(x, k)) for k in df}
        return x.__class__(**fields)

    return x


def _decode_uXXXX(s, pos):
    esc = s[pos + 1 : pos + 5]
    if len(esc) == 4 and esc[1] not in {'x', 'X', b'x', b'X'}:
        try:
            return int(esc, 16)
        except ValueError:
            pass
    raise JSONDecodeError('Invalid \\uXXXX escape', s, pos)


_compile = functools.partial(re.compile, flags=decoder.FLAGS)

UNQUOTERS = (
    (Unquoter(), to_bytes(Unquoter())),
    (Unquoter().to_single(), to_bytes(Unquoter().to_single())),
)
