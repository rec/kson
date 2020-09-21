import base64


def formatter(items: list, binary: bool, options: object):
    quote = '"' if options.double_quote else "'"
    ind = options.ident * ' '
    marker = options.binary_marker
    indent = ''
    item_separator, key_separator = options.separators or (', ', ': ')

    for i in items:
        if not isinstance(i, str):
            if binary:
                yield from ('<', marker, '>', i, '</', marker, '>')
            else:
                yield from ('a', quote, base64.b85decode(i).encode(), quote)

        elif i in '[{':
            yield i
            if ind:
                indent += ind

        elif i in ']}':
            if options.trailing_commas:
                yield ','
            if ind:
                indent = indent[options.indent:]
                yield from ('\n', indent)
            yield i

        elif i == ',':
            if ind:
                yield from (i, '\n', indent)
            else:
                yield item_separator

        elif i == ':':
            yield from (i, key_separator)

        else:
            yield i
