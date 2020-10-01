from json import JSONDecodeError


def unquote(s, strict=False):
    from . import quotes

    s = getattr(s, 'value', s)
    q = quotes.quotes(s)
    chunks = []
    end = 1

    while end:
        end = _unquote_once(q, s, chunks, strict, end)

    return q.quote[:0].join(chunks)


def _unquote_once(quotes, s, chunks, strict, end):
    def error(msg, *items):
        ss = s if isinstance(s, str) else s.decode()
        return JSONDecodeError(msg.format(*items), ss, end)

    def decode_uXXXX(pos):
        esc = s[pos + 1 : pos + 5]
        if len(esc) == 4 and esc[1] not in {'x', 'X', b'x', b'X'}:
            try:
                return int(esc, 16)
            except ValueError:
                pass
        raise error('Invalid \\uXXXX escape')

    chunk = quotes.string_chunk_re.match(s, end)
    if not chunk:
        raise error('Unterminated string')

    # `content` is zero or more unescaped string characters.
    #
    # `term` is the end of string, a literal control character,
    # or a backslash denoting that an escape sequence follows.
    #
    content, term = chunk.groups()
    chunks.append(content)
    if term == quotes.quote:
        return

    end = chunk.end()

    if term != '\\':
        if strict:
            raise error('Invalid control character {0!r} at', term)

        chunks.append(term)
        return end

    try:
        esc = s[end : end + 1]
    except IndexError:
        raise error('Unterminated string') from None

    # If it's not a unicode escape sequence, it should be in the lookup table
    if esc != quotes.unicode_marker:
        try:
            char = quotes.backslash_dict[esc]
        except KeyError:
            raise error('Invalid \\escape: {0!r}', esc) from None

        chunks.append(char)
        return end + 1

    uni = decode_uXXXX(end)
    end += 5
    ucode = '\\' + quotes.unicode_marker

    if 0xD800 <= uni <= 0xDBFF and s[end : end + 2] == ucode:
        uni2 = decode_uXXXX(end + 1)
        if 0xDC00 <= uni2 <= 0xDFFF:
            uni = 0x10000 + (((uni - 0xD800) << 10) | (uni2 - 0xDC00))
            end += 6
    char = chr(uni) if isinstance(s, str) else bytes([uni])
    chunks.append(char)

    return end
