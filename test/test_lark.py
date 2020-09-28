import lark
import unittest


class LarkTest(unittest.TestCase):
    def test_string(self):
        s = parse('0', use_bytes=False)
        assert s == '0'  # OK!

    def test_bin(self):
        s = parse(b'0', use_bytes=True)
        assert s == "b'0'"  # ???
        assert len(s) == 4  # ???


class Transformer(lark.Transformer):
    @lark.v_args(inline=True)
    def integer(self, x):
        return x


def parse(s, use_bytes):
    parse = lark.Lark(
        GRAMMAR, transformer=Transformer(), parser='lalr', use_bytes=use_bytes
    ).parse
    return parse(s)


GRAMMAR = """
?start: value+
?value: integer
integer: SIGNED_INT
%import common.SIGNED_INT
"""
