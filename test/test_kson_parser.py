from kson.grammar.kson import UnexpectedCharacters
from kson.read import decoder
import unittest

parse = decoder.DECODER


class KsonParserTest(unittest.TestCase):
    def test_comma_list(self):
        for e in '[1,]', '[,1]', '[,1,]':
            assert parse(e) == [1]
        with self.assertRaises(TypeError):
            assert parse('[,]' == [])

    def test_comma_object(self):
        for e in '{"one": 1,}', '{,"one": 1}', '{,"one": 1,}':
            assert parse(e) == {'one': 1}
        with self.assertRaises(TypeError):
            assert parse('{,}' == {})

    def test_comment(self):
        test_json = '{"hello": 1 # comment\n}'
        assert parse(test_json) == {"hello": 1}

    def test_single_quote(self):
        assert parse("'hello'") == 'hello'

    def test_quote_backquoted(self):
        assert parse(r'"he\"llo"') == 'he"llo'
        assert parse(r'"he\\\"llo"') == 'he\\\"llo'
        assert parse(r'"he\\"') == 'he\\'

    def test_single_quote_backquoted(self):
        assert parse("'he\\'llo'") == 'he\'llo'
        assert parse("'he\\\\\"llo'") == r'he\"llo'

    def test_double_quote_backquoted(self):
        assert parse('"he\\\\\'llo"') == r"he\'llo"
        assert parse('"he\\"llo"') == "he\"llo"

    def test_binary(self):
        test_json = '`marker`binary`marker`'
        with self.assertRaises(UnexpectedCharacters):
            parse(test_json)

    def test_streaming(self):
        test_json = '"hello"'
        assert parse(test_json) == "hello"

        test_json = '"hello" "hello"'
        assert parse(test_json) == ("hello", "hello")

    def test_end_of_line(self):
        # THIS SHOULD FAIL!
        test_json = '{"long": "two\\\nparts"}'
        with self.assertRaises(UnexpectedCharacters):
            parse(test_json)

    def test_astring(self):
        import base64

        data = bytes(range(256))
        a = base64.b85encode(data)
        a = ''.join(chr(i) for i in a)

        assert list(parse('a"%s"' % a)) == list(data)

    def test_bstring(self):
        assert parse(b"b'to'abc'to'") == b'abc'
        assert parse(b'b"to"abc"to"') == b'abc'
        with self.assertRaises(Exception):
            parse('<to>abc</to>')

    def test_non_finite_numbers(self):
        for i in '[nan, inf, -inf]', '[NaN, Infinity, -Infinity]':
            nan, inf, minus_inf = parse(i)
            assert nan != nan
            assert inf == float('inf')
            assert minus_inf == -inf

        for i in 'NAN', 'nAn', 'Inf', 'infinity', '--inf':
            with self.assertRaises(Exception):
                parse(i)
