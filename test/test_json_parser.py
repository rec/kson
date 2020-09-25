from kson.read.parser import parse_json as parse
import json
import lark
import unittest


class JsonParserTest(unittest.TestCase):
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

    def test_quote_backquoted(self):
        assert parse(r'"he\"llo"') == 'he"llo'
        assert parse(r'"he\\\"llo"') == 'he\\\\\"llo'
        with self.assertRaises(lark.UnexpectedCharacters):
            parse(r'"he\\"llo"') == "he\"llo"
        assert parse(r'"he\\"') == r'he\\'

    def test_comma(self):
        for e in '[1,]', '[,1]', '[,1,]':
            with self.assertRaises(lark.UnexpectedToken):
                parse(e)

    def test_comment(self):
        test_json = '{"hello": 1 # comment\n}'
        with self.assertRaises(lark.UnexpectedCharacters):
            parse(test_json)

    def test_single_quote(self):
        test_json = "'hello'"
        with self.assertRaises(lark.UnexpectedCharacters):
            parse(test_json)

    def test_binary(self):
        test_json = '`marker`binary`marker`'
        with self.assertRaises(lark.UnexpectedCharacters):
            parse(test_json)

    def test_streaming(self):
        test_json = '"hello" "hello"'
        with self.assertRaises(lark.UnexpectedToken):
            parse(test_json)

    def test_end_of_line(self):
        test_json = '{"long": "two\\\nparts"}'
        with self.assertRaises(lark.UnexpectedCharacters):
            parse(test_json)
