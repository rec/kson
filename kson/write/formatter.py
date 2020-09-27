import base64
import os


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

    for i, previous in _with_previous(items):
        if not isinstance(i, str):
            if binary:
                yield from ('b', quote, marker, quote, i, quote, marker, quote)
            else:
                yield from ('a', quote, base64.b85decode(i).encode(), quote)

        elif i in '[{':
            yield i
            if one_indent:
                indent += one_indent
                yield indent

        elif i in ']}':
            if trailing_commas and previous not in '[{':
                yield ','
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


def _with_previous(it):
    previous = None
    for i in it:
        yield i, previous
        previous = i
