from .decoder import Decoder
import functools


def decoder(
    object_hook=None,
    parse_float=None,
    parse_int=None,
    parse_constant=None,
    object_pairs_hook=None,
):
    decoder = Decoder()

    if object_pairs_hook:
        decoder.object = lambda *a: object_pairs_hook(a)

    elif object_hook:
        def oh(*args):
            return object_hook(dict(args))

        decoder.object = oh

    if parse_float:
        decoder.floating = parse_float

    if parse_int:
        decoder.integer = parse_int

    if parse_constant:
        decoder.nan = lambda: parse_constant('NaN')
        decoder.inf = lambda: parse_constant('Infinity')
        decoder.minus_inf = lambda: parse_constant('-Infinity')

    return decoder


def loads(
    s,
    *,
    object_hook=None,
    parse_float=None,
    parse_int=None,
    parse_constant=None,
    object_pairs_hook=None
):
    """
    Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a KSON document) to a Python object.

    ``object_hook`` is an optional function that will be called with the
    result of any object literal decode (a ``dict``). The return value of
    ``object_hook`` will be used instead of the ``dict``. This feature
    can be used to implement custom decoders (e.g. JSON-RPC class hinting).

    ``object_pairs_hook`` is an optional function that will be called with the
    result of any object literal decoded with an ordered list of pairs.  The
    return value of ``object_pairs_hook`` will be used instead of the ``dict``.
    This feature can be used to implement custom decoders.  If ``object_hook``
    is also defined, the ``object_pairs_hook`` takes priority.

    ``parse_float``, if specified, will be called with the string
    of every JSON float to be decoded. By default this is equivalent to
    float(num_str). This can be used to use another datatype or parser
    for JSON floats (e.g. decimal.Decimal).

    ``parse_int``, if specified, will be called with the string
    of every JSON int to be decoded. By default this is equivalent to
    int(num_str). This can be used to use another datatype or parser
    for JSON integers (e.g. float).

    ``parse_constant``, if specified, will be called with one of the
    following strings: -Infinity, Infinity, NaN.
    This can be used to raise an exception if invalid JSON numbers
    are encountered.
    """
    d = decoder(
        object_hook, parse_float, parse_int, parse_constant, object_pairs_hook
    )
    return d(s)


@functools.wraps(loads)
def load(fp, **kwargs):
    """
    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a KSON document) to a Python object.
    """
    return loads(fp.read(), **kwargs)
