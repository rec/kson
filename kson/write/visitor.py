from . visited import visited
from .. import quote
import functools
import math


class Visitor:
    def __init__(self, options):
        self._check_circular = visited(options.check_circular)
        self._quote = quote.Quote(options.single_quote)
        self.options = options

    def visit(self, x):
        return _visit(x, self)

    def quote(self, x):
        return self._quote.add(x, self.options.ensure_ascii)


@functools.singledispatch
def _visit(x, visitor):
    if not visitor.options.default:
        raise TypeError('Cannot visit %s' % type(x))
    yield visitor.options.default(x)


@_visit.register(type(None))
def _(x, visitor):
    yield 'null'


@_visit.register(bool)
def _(x, visitor):
    yield 'true' if x else 'false'


@_visit.register(int)
def _(x, visitor):
    yield repr(x)


@_visit.register(float)
def _(x, visitor):
    if x != x:
        f = 'nan'
    elif x == math.inf:
        f = 'inf'
    elif x == -math.inf:
        f = '-inf'
    else:
        return repr(x)
    if visitor.options.allow_nan:
        return f
    raise ValueError('Out of range float value: %r' % x)


@_visit.register(str)
def _(x, visitor):
    yield visitor.quote(x)


@_visit.register(bytearray)
@_visit.register(bytes)
def _(x, visitor):
    yield x


@_visit.register(list)
def _(x, visitor):
    visitor._check_circular(x)
    yield '['

    for item in x:
        yield from _visit(item, visitor)
        yield ','
    yield ']'


@_visit.register(dict)
def _(x, visitor):
    visitor._check_circular(x)
    yield '{'

    items = x.items()
    if visitor.options.sort_keys:
        items = sorted(items)

    for k, v in items:
        if not isinstance(k, (str, bytes)):
            if visitor.options.skipkeys:
                continue
            raise TypeError('Keys must be strings')

        yield visitor.quote(k)
        yield ':'
        yield from _visit(v, visitor)
        yield ','
    yield '}'
