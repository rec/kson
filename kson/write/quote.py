import json
import re


def quote(double_quote):
    return _DOUBLE if double_quote else _SINGLE


class _Double:
    def __init__(self):
        self.escape = json.ESCAPE
        self.escape_dict = dict(json.ESCAPE_DCT)
        self.quote = '"'

    def _replace(self, match):
        return self.escape_dict[match.group(0)]

    def __call__(self, x):
        return self.quote, self.escape.sub(self._replace, x), self.quote


class _Single(_Double):
    def __init__(self):
        super().__init__()
        self.quote = '\''
        self.escape = re.compile(self.escape.replace('"', "'"))

        self.escape_dict["'"] = "\\'"
        del self.escape_dict['"']


_SINGLE = _Single()
_DOUBLE = _Double()
