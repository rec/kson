import base64


def formatter(items: list, options: object, binary: bool = False):
    quote = '"' if options.double_quote else "'"
    ind = options.ident * ' '
    marker = options.binary_marker
    indent = '\n'
    if options.separators:
        item_separator, key_separator = options.separators
    elif binary:
        item_separator, key_separator = ',:'
    else:
        item_separator, key_separator = ', ', ': '
    previous = ''

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
                yield indent

        elif i in ']}':
            if options.trailing_commas and previous not in '[{':
                yield ','
            if ind:
                indent = indent[:-options.indent]
            yield i

        elif i == ',':
            yield i + indent if ind else item_separator

        elif i == ':':
            yield key_separator

        else:
            yield i

        previous = i
