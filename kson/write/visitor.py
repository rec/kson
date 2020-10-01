from ..quote import quote
import functools
import math


class Visitor:
    def __init__(self, options):
        self._visited = set() if options.check_circular else None
        self.quote = quote.quoter(options.double_quote, options.ensure_ascii)
        self.options = options

    def _check_circular(self, x):
        if self._visited is not None:
            i = id(x)
            if i in self._visited:
                raise ValueError('Circular reference detected')
            self._visited.add(i)

    @functools.singledispatchmethod
    def visit(self, x):
        if self.options.default:
            return self.options.default(x)
        raise TypeError('Cannot visit %s' % type(x))

    @visit.register
    def _(self, x: type(None)):
        yield 'null'

    @visit.register
    def _(self, x: bool):
        yield 'true' if x else 'false'

    @visit.register
    def _(self, x: int):
        yield repr(x)

    @visit.register
    def _(self, x: float):
        if x != x:
            f = 'nan'
        elif x == math.inf:
            f = 'inf'
        elif x == -math.inf:
            f = '-inf'
        else:
            return repr(x)
        if self.options.allow_nan:
            return f
        raise ValueError('Out of range float value: %r' % x)

    @visit.register
    def _(self, x: str):
        yield self.quote(x)

    @visit.register(bytes)
    @visit.register(bytearray)
    def _(self, x):
        yield x

    @visit.register
    def _(self, x: list):
        self._check_circular(x)
        yield '['

        for item in x:
            yield from self.visit(item)
            yield ','
        yield ']'

    @visit.register
    def _(self, x: dict):
        self._check_circular(x)
        yield '{'

        items = x.items()
        if self.options.sort_keys:
            items = sorted(items)

        for k, v in items:
            if not isinstance(k, (str, bytes)):
                if self.options.skipkeys:
                    continue
                raise TypeError('Keys must be strings')

            yield self.quote(k)
            yield ':'
            yield from self.visit(v)
            yield ','
        yield '}'
