from kson import parser
import json
import lark
import unittest

parse = parser.make_parser('grammar/kson.lark')


class KsonParserTest(unittest.TestCase):
    def test_original(self):
        test_json = """
            {
                "empty_object" : {},
                "empty_array"  : [],
                "booleans"     : { "YES" : true, "NO" : false },
                "numbers"      : [ 0, 1, -2, 3.3, 4.4e5, 6.6e-7 ],
                "strings"      : [ "This", [ "And" , "That", "And a \\"b" ] ],
                "nothing"      : null
            }
        """
        j = parse(test_json)
        assert j == json.loads(test_json)

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

    def test_single_quote_backquoted(self):
        assert parse(r"'he\'llo'") == 'he\'llo'
        assert parse(r"'he\"llo'") == r'he\"llo'

    def test_double_quote_backquoted(self):
        assert parse(r'"he\'llo"') == r"he\'llo"
        assert parse(r'"he\"llo"') == "he\"llo"

    def test_binary(self):
        test_json = '`marker`binary`marker`'
        with self.assertRaises(lark.UnexpectedCharacters):
            parse(test_json)

    def test_streaming(self):
        test_json = '"hello"'
        assert parse(test_json) == "hello"

        test_json = '"hello" "hello"'
        assert parse(test_json).children == ["hello", "hello"]
