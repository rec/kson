from kson.read import decoder
from kson.write import writer
import json
import unittest


class RoundTripTest(unittest.TestCase):
    def test_json(self):
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
        j = decoder.DECODER(test_json)
        assert j == json.loads(test_json)

        s = writer.dumps(j)
        j2 = decoder.DECODER(s)
        assert j2 == j

        s2 = writer.dumps(j2)
        assert s == s2

        assert s == EXPECTED

        s3 = writer.dumps(j2, indent=2)

        print('---')
        print(s3)
        print('---')

        assert s3 == EXPECTED2
        j3 = decoder.DECODER(s3)
        assert j2 == j3

    def test_indent1(self):
        items = []

        s = writer.dumps(items, indent=2)
        assert s == '[\n]\n'

    def test_indent2(self):
        items = [1]

        s = writer.dumps(items, indent=2)
        assert s == '[\n  1,\n]\n'

    def test_indent3(self):
        items = [1, [2, [3, 4], 5], 6]

        s = writer.dumps(items, indent=2)

        assert s == EXPECTED3


EXPECTED = """\
{'empty_object': {}, \
'empty_array': [], \
'booleans': {'YES': true, 'NO': false}, \
'numbers': [0, 1, -2, 3.3, 440000.0, 6.6e-07], \
'strings': ['This', ['And', 'That', 'And a "b']], \
'nothing': null}
"""

EXPECTED2 = """\
{
  'empty_object': {
  },
  'empty_array': [
  ],
  'booleans': {
    'YES': true,
    'NO': false,
  },
  'numbers': [
    0,
    1,
    -2,
    3.3,
    440000.0,
    6.6e-07,
  ],
  'strings': [
    'This',
    [
      'And',
      'That',
      'And a "b',
    ],
  ],
  'nothing': null,
}
"""

EXPECTED3 = """[
  1,
  [
    2,
    [
      3,
      4,
    ],
    5,
  ],
  6,
]
"""
