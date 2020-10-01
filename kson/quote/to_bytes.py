from json import decoder
import functools
import re

compile_re = functools.partial(re.compile, flags=decoder.FLAGS)


def to_bytes(x):
    if isinstance(x, str):
        return x.encode()
    if isinstance(x, list):
        return [to_bytes(i) for i in x]
    if isinstance(x, dict):
        return {to_bytes(k): to_bytes(v) for k, v in x.items()}
    if isinstance(x, re.Pattern):
        return compile_re(to_bytes(x.pattern))

    df = getattr(x, "__dataclass_fields__", None)
    if df is not None:
        fields = {k: to_bytes(getattr(x, k)) for k in df}
        return x.__class__(**fields)

    return x
