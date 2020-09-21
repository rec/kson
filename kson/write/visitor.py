import functools
import json
from . import quote


class Visitor:
    def __init__(self, options):
        self.options = options
        self._visited = {}
        self._quote = quote.DOUBLE if options.double_quote else quote.SINGLE

    def _visit(self, x):
        if self.options.check_circular:
            i = id(x)
            if i in self._visited:
                raise ValueError('Circular reference detected')
            self._visited.add(i)

    @functools.singledispatchmethod
    def visit(self, x):
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
            return 'NaN'
        if x == json.INFINITY:
            return 'Infinity'
        if x == -json.INFINITY:
            return '-Infinity'
        return repr(x)

    @visit.register
    def _(self, x: str):
        yield self._quote(x)

    @visit.register(bytes)
    @visit.register(bytearray)
    def _(self, x):
        yield x

    @visit.register
    def _(self, x: list):
        self._visit(x)
        yield '['
        for i, item in enumerate(x):
            if i:
                yield ','
            yield from self.visit(item)
        if not i and self.options.trailing_commas:
            yield ','
        yield ']'

    @visit.register
    def _(self, x: dict):
        self._visit(x)
        yield '{'

        it = sorted(x.items()) if self.options.sort_keys else x.items()
        for i, (k, v) in enumerate(it):
            if i:
                yield ','
            if not isinstance(k, str):
                raise TypeError('Keys must be strings')
            yield from self.visit(k)
            yield ':'
            yield from self.visit(v)
        if not i and self.options.trailing_commas:
            yield ','
        yield '}'
