from kson.quote import to_bytes
from kson.read import decoder
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

        print("---")
        print(s3)
        print("---")

        assert s3 == EXPECTED2
        j3 = decoder.DECODER(s3)
        assert j2 == j3

    def test_json_bytes(self):
        assert decoder.DECODER('"\\"b"') == '"b'
        assert decoder.DECODER(b"true") is True
        assert decoder.DECODER(b"[]") == []
        assert decoder.DECODER(b"{}") == {}
        assert decoder.DECODER(b"''") == b""
        assert decoder.DECODER(b'""') == b""

    def test_bytes_json(self):
        expected = writer.dumps('"b', use_bytes=True, double_quote=True)
        assert b'"\\"b"' == expected
        assert b"true" == writer.dumps(True, use_bytes=True)
        assert b"[]" == writer.dumps([], use_bytes=True)
        assert b"{}" == writer.dumps({}, use_bytes=True)
        assert b"''" != writer.dumps(b"", use_bytes=True)  # FIX
        assert b'""' != writer.dumps(b"", use_bytes=True)

    def test_json_bytes_XXX(self):
        assert b'""' != writer.dumps(b"", use_bytes=True)

    def NO_test_json_bytes_full(self):
        j = decoder.DECODER(TEST_JSON.encode())
        assert j == to_bytes.to_bytes(json.loads(TEST_JSON))

        s = writer.dumps(j)
        j2 = decoder.DECODER(s)
        assert j2 == j

        s2 = writer.dumps(j2)
        assert s == s2

        assert s == EXPECTED.encode()

        s3 = writer.dumps(j2, indent=2)

        print("---")
        print(s3)
        print("---")

        assert s3 == EXPECTED2.encode()
        j3 = decoder.DECODER(s3)
        assert j2 == j3

    def test_indent1(self):
        items = []

        s = writer.dumps(items, indent=2)
        assert s == "[\n]\n"

    def test_indent2(self):
        items = [1]

        s = writer.dumps(items, indent=2)
        assert s == "[\n  1,\n]\n"

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
