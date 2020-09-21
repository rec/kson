import functools
import json


class Visitor:
    def __init__(self, check_circular, quote, sort_keys):
        self._visited = {} if check_circular else None
        self.quote = quote
        self.sort_keys = sort_keys

    def _visit(self, x):
        if self._visited is not None:
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
        yield self.quote(x)

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
        yield ']'

    @visit.register
    def _(self, x: dict):
        self._visit(x)
        yield '{'

        items = x.items()
        if self.sort_keys:
            items = sorted(items)
        for i, (k, v) in enumerate(items):
            if i:
                yield ','
            if not isinstance(k, str):
                raise TypeError('Keys must be strings')
            yield self.quote(k)
            yield ':'
            yield from self.visit(v)
        yield '}'
