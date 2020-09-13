import json
import unittest
import parser
import json_parser

parse = parser.make_parser(json_parser)


class JsonParserTest(unittest.TestCase):
    def test_same(self):
        test_json = '''
            {
                "empty_object" : {},
                "empty_array"  : [],
                "booleans"     : { "YES" : true, "NO" : false },
                "numbers"      : [ 0, 1, -2, 3.3, 4.4e5, 6.6e-7 ],
                "strings"      : [ "This", [ "And" , "That", "And a \\"b" ] ],
                "nothing"      : null
            }
        '''

        j = parse(test_json)
        assert j == json.loads(test_json)
