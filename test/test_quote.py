from json import JSONDecodeError
from kson import quote
import functools
import unittest


def quoter(single_quote=False, ensure_ascii=False):
    q = quote.Quote(single_quote)
    return functools.partial(q.add, ensure_ascii=ensure_ascii)


single = quoter(single_quote=True)
single_ascii = quoter(single_quote=True, ensure_ascii=True)
double = quoter()
double_ascii = quoter(ensure_ascii=True)


def round_trip(quoter, raw, quoted):
    assert quoter(raw) == quoted
    assert quote.unquote(quoted) == raw, quoted


class QuoteTest(unittest.TestCase):
    def test_near_trivial(self):
        assert quote.unquote("'\\''") == "'"

    def test_empty(self):
        round_trip(single, '', "''")
        round_trip(single_ascii, '', "''")
        round_trip(double, '', '""')
        round_trip(double_ascii, '', '""')

    def test_single(self):
        round_trip(single, ' ', "' '")
        round_trip(single_ascii, ' ', "' '")
        round_trip(double, ' ', '" "')
        round_trip(double_ascii, ' ', '" "')

    def test_quote1(self):
        round_trip(single, "'", "'\\''")
        round_trip(single_ascii, "'", "'\\''")
        round_trip(double, "'", '"\'"')
        round_trip(double_ascii, "'", '"\'"')

    def test_quote2(self):
        round_trip(single, '"', "'\"'")
        round_trip(single_ascii, '"', "'\"'")
        round_trip(double, '"', '"\\""')
        round_trip(double_ascii, '"', '"\\""')

    def test_escape_error(self):
        with self.assertRaises(JSONDecodeError) as m:
            quote.unquote('"\\u17"')
        expected = 'Invalid \\uXXXX escape: line 1 column 3 (char 2)'
        assert m.exception.args[0] == expected

    def test_escape_error2(self):
        with self.assertRaises(JSONDecodeError) as m:
            quote.unquote('"\\u17NO"')
        expected = 'Invalid \\uXXXX escape: line 1 column 3 (char 2)'
        assert m.exception.args[0] == expected

    def test_escape_error3(self):
        with self.assertRaises(JSONDecodeError) as m:
            quote.unquote('"\\u17')
        expected = 'Invalid \\uXXXX escape: line 1 column 3 (char 2)'
        assert m.exception.args[0] == expected

    def test_missing_quote(self):
        for x in '"hello', "'hello":
            with self.assertRaises(JSONDecodeError) as m:
                quote.unquote(x)
            expected = 'Unterminated string: line 1 column 2 (char 1)'
            assert m.exception.args[0] == expected
        with self.assertRaises(JSONDecodeError) as m:
            quote.unquote("'hello\\'")
        expected = 'Unterminated string: line 1 column 9 (char 8)'
        assert m.exception.args[0] == expected

    def test_bad_escape(self):
        for x in '"\\z"', "'\\z'":
            with self.assertRaises(JSONDecodeError) as m:
                quote.unquote(x)
            expected = "Invalid \\escape: 'z': line 1 column 3 (char 2)"
            assert m.exception.args[0] == expected

    def test_backslashes(self):
        round_trip(single, '\n', "'\\n'")
        round_trip(single_ascii, '\n', "'\\n'")
        round_trip(double, '\n', '"\\n"')
        round_trip(double_ascii, '\n', '"\\n"')

    def test_more_backslashes(self):
        round_trip(single, '\\n', "'\\\\n'")
        round_trip(double, '\\n', '"\\\\n"')
        round_trip(single, '\\\n', "'\\\\\\n'")
        round_trip(double, '\\\n', '"\\\\\\n"')
        round_trip(single, '\\\\n', "'\\\\\\\\n'")
        round_trip(double, '\\\\n', '"\\\\\\\\n"')
        round_trip(single, '\\\\\n', "'\\\\\\\\\\n'")
        round_trip(double, '\\\\\n', '"\\\\\\\\\\n"')
        round_trip(single, '\\\\\n', "'\\\\\\\\\\n'")
        round_trip(double, '\\\\\n', '"\\\\\\\\\\n"')

    def test_extended(self):
        round_trip(single, '🔑', "'🔑'")
        round_trip(single_ascii, '🔑', "'\\ud83d\\udd11'")
        round_trip(double, '🔑', '"🔑"')
        round_trip(double_ascii, '🔑', '"\\ud83d\\udd11"')

    def test_quoter(self):
        round_trip(quoter(True, False), '🔑', "'🔑'")
        round_trip(quoter(True, True), '🔑', "'\\ud83d\\udd11'")
        round_trip(quoter(False, False), '🔑', '"🔑"')
        round_trip(quoter(False, True), '🔑', '"\\ud83d\\udd11"')
