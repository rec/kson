from .formatter import formatter
from .options import Options
from .visited import visited
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


def needs_bytes(x, visit):
    if isinstance(x, (bytearray, bytes)):
        return True

    if isinstance(x, list):
        visit(x)
        return any(needs_bytes(i, visit) for i in x)

    if isinstance(x, dict):
        visit(x)
        return any(needs_bytes(i, visit) for i in x.values())

    return False


def dumps(obj, use_bytes=None, **kwargs):
    if use_bytes is None:
        visit = visited(kwargs.get('check_circular', True))
        use_bytes = needs_bytes(obj, visit)
    fp = io.BytesIO() if use_bytes else io.StringIO()
    dump(obj, fp, **kwargs)
    return fp.getvalue()
