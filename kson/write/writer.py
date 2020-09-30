from .formatter import formatter
from .options import Options
from .visitor import Visitor
import io


def write_items(items, fp, options):
    use_bytes = not hasattr(fp, 'newlines')
    written = 0

    for i in items:
        parts = Visitor(options).visit(i)
        for part in formatter(parts, options, use_bytes):
            if use_bytes and isinstance(part, str):
                part = part.encode()
            written += fp.write(part)

    return written


def dump(obj, fp, **kwargs):
    """Serialize ``obj`` as a KSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).
    """
    return write_items([obj], fp, Options(**kwargs))


def has_use_bytes(obj):
    def contents(x):
        if isinstance(x, list):
            for i in x:
                yield from contents(i)
        if isinstance(x, dict):
            for k, v in x.items():
                yield from contents(k)
                yield from contents(v)
        yield x

    for i in contents(obj):
        if isinstance(i, str):
            return False
        if isinstance(i, (bytes, bytearray)):
            return True


def dumps(obj, use_bytes=None, **kwargs):
    if use_bytes is None:
        use_bytes = has_use_bytes(obj)
    fp = io.BytesIO() if use_bytes else io.StringIO()
    dump(obj, fp, **kwargs)
    return fp.getvalue()
