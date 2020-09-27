import base64
import os

OPENING, CLOSING = '[{', ']}'


def formatter(items, options, binary):
    quote = '"' if options.double_quote else "'"
    one_indent = options.indent * ' '
    marker = options.binary_marker
    indent = '\n'
    if options.trailing_commas is not None:
        trailing_commas = options.trailing_commas
    else:
        trailing_commas = bool(options.indent)

    if options.separators:
        item_separator, key_separator = options.separators
    elif binary:
        item_separator, key_separator = ',', ':'
    else:
        item_separator, key_separator = ', ', ': '

    for behind, i, ahead in _look_ahead_behind(items):
        if not isinstance(i, str):
            if binary:
                yield from ('b', quote, marker, quote, i, quote, marker, quote)
            else:
                yield from ('a', quote, base64.b85decode(i).encode(), quote)

        elif i in OPENING:
            yield i
            if one_indent:
                indent += one_indent
                yield indent

        elif i in CLOSING:
            if trailing_commas and behind not in OPENING:
                yield ',' + indent
            if one_indent:
                indent = indent[:-options.indent]
            yield i

        elif i == ',':
            if one_indent:
                yield i + indent
            else:
                yield item_separator

        elif i == ':':
            yield key_separator

        else:
            yield i

    if options.record_end is not None:
        yield options.record_end
    elif not binary:
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
