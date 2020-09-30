import base64
import os

OPENING, CLOSING = '[{', ']}'


def formatter(items, options, use_bytes):
    quote = '"' if options.double_quote else "'"
    one_indent = options.indent * ' '
    marker = options.binary_marker
    newline = '\n'
    indent = ''
    if options.trailing_commas is not None:
        trailing_commas = options.trailing_commas
    else:
        trailing_commas = bool(options.indent)

    if options.separators:
        item_separator, key_separator = options.separators
    elif use_bytes:
        item_separator, key_separator = ',', ':'
    else:
        item_separator, key_separator = ', ', ': '

    for behind, i, ahead in _look_ahead_behind(items):
        old_indent = indent
        if not isinstance(i, str):
            if use_bytes:
                yield from ('b', quote, marker, quote, i, quote, marker, quote)
            else:
                yield from ('a', quote, base64.b85decode(i).encode(), quote)

        elif i in OPENING:
            yield i
            if options.indent:
                indent += one_indent
                yield newline
                yield old_indent if ahead in CLOSING else indent

        elif i in CLOSING:
            indent = indent[: -options.indent]
            if trailing_commas and behind not in OPENING:
                yield ','
                if options.indent:
                    yield newline
                    # yield old_indent if ahead in CLOSING else indent
                    yield indent
            yield i

        elif i == ',':
            if options.indent:
                yield i
                yield newline
                yield indent[: -options.indent] if ahead in CLOSING else indent
            else:
                yield item_separator

        elif i == ':':
            yield key_separator

        else:
            yield i

    if options.record_end is not None:
        yield options.record_end
    elif not use_bytes:
        yield os.linesep


def _look_ahead_behind(it, none=''):
    empty = it
    behind = current = empty
    for i in it:
        if current is not empty:
            if behind is empty:
                behind = none
            yield behind, current, i
            behind = current
        current = i
    if current is not empty:
        yield behind, current, none
