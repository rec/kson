from .to_bytes import to_bytes, compile_re
from dataclasses import dataclass, field
from json import decoder, JSONDecodeError
import re

SINGLE = "'"
DOUBLE = '"'


def unquote(s, strict=False):
    use_bytes = not isinstance(s, str)
    is_single_quote = s[0] in {SINGLE, SINGLE.encode()}

    unquoter = UNQUOTERS[is_single_quote][use_bytes]
    return unquoter.unquote(s, strict)


@dataclass
class Unquoter:
    quote: object = DOUBLE
    backslash: object = "\\"
    string_chunk_re: object = decoder.STRINGCHUNK
    backslash_dict: dict = field(default_factory=decoder.BACKSLASH.copy)
    unicode_marker: object = "u"

    def to_single(self):
        u = Unquoter()
        for k in self.__dataclass_fields__:
            v = getattr(self, k)
            if isinstance(v, str):
                v = v.replace(DOUBLE, SINGLE)
            elif isinstance(v, re.Pattern):
                v = compile_re(v.pattern.replace(DOUBLE, SINGLE))
            elif isinstance(v, dict):
                v.pop(DOUBLE, None)
                v[SINGLE] = SINGLE
            else:
                raise TypeError
            setattr(u, k, v)
        return u

    def unquote(self, s, strict=False):
        s = getattr(s, "value", s)
        chunks = []
        end = 1

        while end:
            end = self._unquote_once(s, chunks, strict, end)
        return self.quote[:0].join(chunks)

    def _unquote_once(self, s, chunks, strict, end):
        chunk = self.string_chunk_re.match(s, end)
        if not chunk:
            raise JSONDecodeError("Unterminated string", s)

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
            esc = s[end : end + 1]
        except IndexError:
            raise JSONDecodeError("Unterminated string", s) from None

        # If not a unicode escape sequence, must be in the lookup table
        if esc != self.unicode_marker:
            try:
                char = self.backslash_dict[esc]
            except KeyError:
                print("ONE", esc, self.backslash_dict, sep=" | ")

                msg = "Invalid \\escape: {0!r}".format(esc)
                if not isinstance(s, str):
                    s = s.decode()
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


def _decode_uXXXX(s, pos):
    esc = s[pos + 1 : pos + 5]
    if len(esc) == 4 and esc[1] not in {"x", "X", b"x", b"X"}:
        try:
            return int(esc, 16)
        except ValueError:
            pass
    raise JSONDecodeError("Invalid \\uXXXX escape", s, pos)


UNQUOTERS = (
    (Unquoter(), to_bytes(Unquoter())),
    (Unquoter().to_single(), to_bytes(Unquoter().to_single())),
)
