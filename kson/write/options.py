from dataclasses import dataclass
import uuid

DEFAULT_MARKER = b'>'

while b'>' in DEFAULT_MARKER:
    DEFAULT_MARKER = uuid.uuid4().bytes


@dataclass
class Options:
    """
    ARGUMENTS
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

      If ``indent`` is a non-negative integer, then KSON array elements and
      object members will be pretty-printed with that indent level.
      ``None`` means that

      ``default(obj)`` is a function that should return a serializable version
      of obj or raise TypeError. The default simply raises TypeError.

      If *sort_keys* is true (default: ``False``), then the output of
      dictionaries will be sorted by key.
    """

    record_end: str = None
    trailing_commas: bool = True
    double_quote: bool = False
    binary_marker: bytes = DEFAULT_MARKER

    # These next parameters have the same meaning as in json.dump
    skipkeys: bool = False
    ensure_ascii: bool = True
    check_circular: bool = True
    allow_nan: bool = True
    indent: int = 0
    separators: object = None
    default: object = None
    sort_keys: bool = False
