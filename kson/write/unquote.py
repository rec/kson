from json import decoder, JSONDecodeError
import re

STRINGCHUNK = re.compile(
    decoder.STRINGCHUNK.pattern.replace('"', "'"), decoder.FLAGS
)
BACKSLASH = dict(decoder.BACKSLASH)
BACKSLASH["'"] = "'"
del BACKSLASH['"']


def unquote(s, strict=False):
    quote = s[0]
    if quote == '"':
        _b = decoder.BACKSLASH
        _m = decoder.STRINGCHUNK.match
    else:
        quote = "'"
        _b = BACKSLASH
        _m = STRINGCHUNK.match

    chunks = []
    _append = chunks.append
    begin = 0
    end = 1
    while 1:
        chunk = _m(s, end)
        if chunk is None:
            raise JSONDecodeError("Unterminated string starting at", s, begin)
        end = chunk.end()
        content, terminator = chunk.groups()
        # Content is contains zero or more unescaped string characters
        if content:
            _append(content)
        # Terminator is the end of string, a literal control character,
        # or a backslash denoting that an escape sequence follows
        if terminator == quote:
            break
        elif terminator != '\\':
            if strict:
                msg = "Invalid control character {0!r} at".format(terminator)
                raise JSONDecodeError(msg, s, end)
            else:
                _append(terminator)
                continue
        try:
            esc = s[end]
        except IndexError:
            raise JSONDecodeError("Unterminated string starting at",
                                  s, begin) from None
        # If not a unicode escape sequence, must be in the lookup table
        if esc != 'u':
            try:
                char = _b[esc]
            except KeyError:
                msg = "Invalid \\escape: {0!r}".format(esc)
                raise JSONDecodeError(msg, s, end)
            end += 1
        else:
            uni = decoder._decode_uXXXX(s, end)
            end += 5
            if 0xd800 <= uni <= 0xdbff and s[end:end + 2] == '\\u':
                uni2 = decoder._decode_uXXXX(s, end + 1)
                if 0xdc00 <= uni2 <= 0xdfff:
                    uni = 0x10000 + (((uni - 0xd800) << 10) | (uni2 - 0xdc00))
                    end += 6
            char = chr(uni)
        _append(char)
    return ''.join(chunks)
