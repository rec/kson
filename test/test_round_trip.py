from kson.read import decoder
from kson.write import writer
import functools
import json
import json.decoder
import kson
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


def round_trip(x, pre, post=None, **kwargs):
    post = pre if post is None else post
    assert kson.loads(pre) == x
    assert kson.dumps(x, **kwargs) == post


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

    def test_json_bytes(self):
        round_trip('"b', '"\\"b"', '\'"b\'')
        round_trip(True, b'true', 'true')
        round_trip([], b'[]', '[]')
        round_trip({}, b'{}', '{}')
        round_trip('', b"''", "''")
        round_trip('', b'""', "''")

    def test_bytes_json(self):
        expected = writer.dumps('"b', use_bytes=True, double_quote=True)
        assert b'"\\"b"' == expected
        assert b'true' == writer.dumps(True, use_bytes=True)
        assert b'[]' == writer.dumps([], use_bytes=True)
        assert b'{}' == writer.dumps({}, use_bytes=True)
        assert b"''" != writer.dumps(b"", use_bytes=True)  # FIX
        assert b'""' != writer.dumps(b"", use_bytes=True)

    def test_json_bytes_full(self):
        j = decoder.DECODER(TEST_JSON.encode())
        j2 = json.loads(TEST_JSON)
        assert j == j2

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

    def test_binary_dump(self):
        items = {'foo': bytes(range(8))}
        dumps = functools.partial(writer.dumps, items, binary_marker=b'ab')
        b = dumps()
        b_bytes = dumps(use_bytes=True)
        b_str = dumps(use_bytes=False)

        assert b == b_bytes
        assert b != b_str
        assert b == b"{'foo':b'ab'\x00\x01\x02\x03\x04\x05\x06\x07'ab'}"
        assert b_str == "{'foo': a'009C61O)~M'}"

    def test_unicode_chars_1(self):
        dumps = functools.partial(writer.dumps, double_quote=True)
        for uni in range(256):
            u = dumps(uni)
            u_ascii = dumps(uni, ensure_ascii=True)
            u_no_ascii = dumps(uni, ensure_ascii=False)

            assert u == u_no_ascii
            assert u_ascii == json.dumps(uni)
            assert u_no_ascii == json.dumps(uni, ensure_ascii=False)


EXPECTED = """\
{'empty_object': {}, \
'empty_array': [], \
'booleans': {'YES': true, 'NO': false}, \
'numbers': [0, 1, -2, 3.3, 440000.0, 6.6e-07], \
'strings': ['This', ['And', 'That', 'And a "b']], \
'nothing': null}"""

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
