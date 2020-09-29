from kson.read import decoder
from kson.read import unquote
from kson.write import writer
import json
import unittest

TEST_JSON = """
{
    "empty_object" : {},
    "empty_array"  : [],
    "booleans"     : { "YES" : true, "NO" : false },
    "numbers"      : [ 0, 1, -2, 3.3, 4.4e5, 6.6e-7 ],
    "strings"      : [ "This", [ "And" , "That", "And a \\"b" ] ],
    "nothing"      : null
}
"""


class RoundTripTest(unittest.TestCase):
    def test_json(self):
        j = decoder.DECODER(TEST_JSON)
        assert j == json.loads(TEST_JSON)

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

    def test_json_binary(self):
        test_json = '"\\"b"'
        decoder.DECODER(test_json)
        test_json = b'"\\"b"'
        decoder.DECODER(test_json)

    def DONT_test_json_binary_full(self):
        j = decoder.DECODER(TEST_JSON.encode())
        assert j == unquote.to_bytes(json.loads(TEST_JSON))

        s = writer.dumps(j)
        j2 = decoder.DECODER(s)
        assert j2 == j

        s2 = writer.dumps(j2)
        assert s == s2

        assert s == EXPECTED.encode()

        s3 = writer.dumps(j2, indent=2)

        print('---')
        print(s3)
        print('---')

        assert s3 == EXPECTED2.encode()
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

EXPECTED3 = """\
[
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
