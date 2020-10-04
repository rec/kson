from kson.grammar import json
import re
import unittest

DOUBLE_QUOTE_RE = re.compile(r'(?<!\\)(\\\\)*\\(")')


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
        import json
        assert j == json.loads(test_json)

    def test_quote_backquoted(self):
        assert parse(r'"he\"llo"') == 'he"llo'
        assert parse(r'"he\\\"llo"') == 'he\\\\\"llo'
        with self.assertRaises(json.UnexpectedCharacters):
            parse(r'"he\\"llo"') == "he\"llo"
        assert parse(r'"he\\"') == r'he\\'

    def test_comma(self):
        for e in '[1,]', '[,1]', '[,1,]':
            with self.assertRaises(json.UnexpectedToken):
                parse(e)

    def test_comment(self):
        test_json = '{"hello": 1 # comment\n}'
        with self.assertRaises(json.UnexpectedCharacters):
            parse(test_json)

    def test_single_quote(self):
        test_json = "'hello'"
        with self.assertRaises(json.UnexpectedCharacters):
            parse(test_json)

    def test_binary(self):
        test_json = '`marker`binary`marker`'
        with self.assertRaises(json.UnexpectedCharacters):
            parse(test_json)

    def test_streaming(self):
        test_json = '"hello" "hello"'
        with self.assertRaises(json.UnexpectedToken):
            parse(test_json)

    def test_end_of_line(self):
        test_json = '{"long": "two\\\nparts"}'
        with self.assertRaises(json.UnexpectedCharacters):
            parse(test_json)


class JsonTransformer(json.Transformer):
    def string(self, s):
        s = s[0]
        return DOUBLE_QUOTE_RE.sub(r'\1' + s[0], s[1:-1])

    array = list
    object = dict
    object_entry = tuple

    def integer(self, s):
        return int(s[0])

    def floating(self, s):
        return float(s[0])

    def null(self, _):
        return None

    def false(self, _):
        return False

    def true(self, _):
        return True


parse = json.Lark_StandAlone(JsonTransformer()).parse
