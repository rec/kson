from . import quotes
from json import JSONDecodeError


def unquote(s, strict=False):
    s = getattr(s, "value", s)
    q = quotes.quotes(s)
    chunks = []
    end = 1

    while end:
        end = _unquote_once(q, s, chunks, strict, end)
    return q.quote[:0].join(chunks)


def _unquote_once(quotes, s, chunks, strict, end):
    chunk = quotes.string_chunk_re.match(s, end)
    if not chunk:
        raise JSONDecodeError("Unterminated string", str(s), end)

    (content, term), end = chunk.groups(), chunk.end()
    # Content is zero or more unescaped string characters
    if content:
        chunks.append(content)
    # Term is the end of string, a literal control character,
    # or a backslash denoting that an escape sequence follows
    if term == quotes.quote:
        return
    if term != quotes.backslash:
        if strict:
            msg = "Invalid control character {0!r} at".format(term)
            raise JSONDecodeError(msg, s, end)
        chunks.append(term)
        return end
    try:
        esc = s[end : end + 1]
    except IndexError:
        raise JSONDecodeError("Unterminated string", str(s), end) from None

    # If not a unicode escape sequence, must be in the lookup table
    if esc != quotes.unicode_marker:
        try:
            char = quotes.backslash_dict[esc]
        except KeyError:
            msg = "Invalid \\escape: {0!r}".format(esc)
            if not isinstance(s, str):
                s = s.decode()
            raise JSONDecodeError(msg, s, end) from None
        else:
            chunks.append(char)
            return end + 1

    uni = _decode_uXXXX(s, end)
    end += 5
    ucode = quotes.backslash + quotes.unicode_marker
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
