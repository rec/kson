from . visitor import Visitor


class Writer:
    def __init__(self, options, fp):
        self.options = options
        self.fp = fp
        self._write = _writer(fp)

    def dump(self, x):
        visitor = Visitor(self.options)
        for i in visitor.visiti(x):
            self._write(i)

        if self.options.record_end:
            self.options.write(self.options.record_end)


def _writer(fp):
    def write_text(s):
        if not isinstance(s, str):
            raise TypeError('Cannot write binary to text stream')
        fp.write(s)

    def write_binary(s):
        if isinstance(s, str):
            s = s.encode()
        fp.write(s)

    return write_text if hasattr(fp, 'newlines') else write_binary
