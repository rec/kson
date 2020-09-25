from kson.read.unquote import unquote
from kson.write.quote import single
from kson.write.quote import single_ascii
from kson.write.quote import double
from kson.write.quote import double_ascii
from kson.write.quote import quoter
import unittest


def round_trip(quoter, raw, quoted):
    assert quoter(raw) == quoted
    assert unquote(quoted) == raw


class QuoteTest(unittest.TestCase):
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

    def test_quote(self):
        round_trip(single, "'", "'\\''")
        round_trip(single_ascii, "'", "'\\''")
        round_trip(double, "'", '"\'"')
        round_trip(double_ascii, "'", '"\'"')

    def test_quote2(self):
        round_trip(single, '"', "'\"'")
        round_trip(single_ascii, '"', "'\"'")
        round_trip(double, '"', '"\\""')
        round_trip(double_ascii, '"', '"\\""')

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
        round_trip(quoter(False, False), '🔑', "'🔑'")
        round_trip(quoter(False, True), '🔑', "'\\ud83d\\udd11'")
        round_trip(quoter(True, False), '🔑', '"🔑"')
        round_trip(quoter(True, True), '🔑', '"\\ud83d\\udd11"')
