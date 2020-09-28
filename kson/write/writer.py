from .formatter import formatter
from .options import Options
from .visitor import Visitor
import io


def write_items(items, fp, options):
    binary = not hasattr(fp, 'newlines')
    written = 0

    for i in items:
        parts = Visitor(options).visit(i)
        for part in formatter(parts, options, binary):
            if binary and isinstance(part, str):
                part = part.encode()
            written += fp.write(part)

    return written


def dump(obj, fp, **kwargs):
    """Serialize ``obj`` as a KSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).
    """
    return write_items([obj], fp, Options(**kwargs))


def dumps(obj, binary=False, **kwargs):
    fp = io.BytesIO() if binary else io.StringIO()
    dump(obj, fp, **kwargs)
    return fp.getvalue()
