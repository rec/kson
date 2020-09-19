import json
import re
import os
import functools


ESCAPE_SINGLE = re.compile(json.ESCAPE.replace('"', "'"))

ESCAPE_DCT_SINGLE = dict(json.ESCAPE_DCT)
ESCAPE_DCT_SINGLE["'"] = "\\'"
del ESCAPE_DCT_SINGLE['"']


def dumper(
        fp, *,
        skipkeys=False,
        check_circular=True,
        allow_nan=True,
        indent=None,
        default=None,
        sort_keys=False,
        record_end=os.linesep,
        trailing_commas=True,
        double_quotes=False,
        binary_marker=None):
    if hasattr(fp, 'newlines'):
        def write(s):
            if not isinstance(s, str):
                raise TypeError('Cannot write')
            fp.write(s)
    else:
        def write(s):
            if isinstance(s, str):
                s = s.encode()
            fp.write(s)

    quote = '"' if double_quotes else "'"
    escape = json.ESCAPE if double_quotes else ESCAPE_SINGLE
    escape_dct = json.ESCAPE_DCT if double_quotes else ESCAPE_DCT_SINGLE
    visited = {}

    @functools.singledispatch
    def dump(x):
        raise TypeError('Cannot dump %s' % type(x))

    @dump.register(str)
    def _(x):
        def replace(match):
            return escape_dct[match.group(0)]

        yield from (quote, escape.sub(replace, x), quote)

    @dump.register(bool)
    def _(x):
        return 'true' if x else 'false'

    @dump.register(type(None))
    def _(x):
        return 'null'

    @dump.register(int)
    def _(x):
        return repr(x)

    @dump.register(float)
    def _(x):
        if x != x:
            text = 'NaN'
        elif x == json.INFINITY:
            text = 'Infinity'
        elif x == -json.INFINITY:
            text = '-Infinity'
        else:
            return repr(x)
        if allow_nan:
            return text
        raise ValueError(
            'Out of range float values are not KSON compliant: ' + repr(x))

    @dump.register(list)
    @dump.register(dict)
    def _(x):
        if check_circular:
            i = id(x)
            if i in visited:
                raise ValueError('Circular reference detected')
            visited.add(i)

        is_list = isinstance(x, list)

        yield '{['[is_list]
        if is_list:
            it = x
        elif sort_keys:
            it = sorted(x.items())
        else:
            it = x.items()
        for i, item in enumerate(it):
            if i:
                yield ','
            if is_list:
                yield from dump(item)
            else:
                k, v = item
                if not isinstance(k, str):
                    raise TypeError('Keys must be strings')
                yield from dump(k)
                yield ':'
                yield from dump(v)
        if not i and trailing_commas:
            yield ','
        yield '}]'[is_list]

    def dumper(x):
        for i in dump(x):
            write(i)

        if record_end:
            write(record_end)


def dump(fp, a):
    """
    Serialize ``obj`` as a JSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).

    If ``skipkeys`` is true then ``dict`` keys that are not basic types
    (``str``, ``int``, ``float``, ``bool``, ``None``) will be skipped
    instead of raising a ``TypeError``.

    If ``ensure_ascii`` is false, then the strings written to ``fp`` can
    contain non-ASCII characters if they appear in strings contained in
    ``obj``. Otherwise, all such characters are escaped in JSON strings.

    If ``check_circular`` is false, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``OverflowError`` (or worse).

    If ``allow_nan`` is false, then it will be a ``ValueError`` to
    serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``)
    in strict compliance of the JSON specification, instead of using the
    JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

    If ``indent`` is a non-negative integer, then JSON array elements and
    object members will be pretty-printed with that indent level. An indent
    level of 0 will only insert newlines. ``None`` is the most compact
    representation.

    ``default(obj)`` is a function that should return a serializable version
    of obj or raise TypeError. The default simply raises TypeError.

    If *sort_keys* is true (default: ``False``), then the output of
    dictionaries will be sorted by key.
    """
    pass
