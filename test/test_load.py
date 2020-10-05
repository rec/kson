from .test_round_trip import TEST_JSON
import io
import json
import kson
import math
import unittest


def loads(loads, text):
    results = []

    def parse_float(x):
        results.append(("parse_float", x))
        return float(x)

    def parse_int(x):
        results.append(("parse_int", x))
        return int(x)

    def parse_constant(x):
        results.append(("parse_constant", x))
        if x == "NaN":
            return math.nan
        if x == "Infinity":
            return math.inf
        if x == "-Infinity":
            return -math.inf
        raise ValueError("%s" % x)

    def object_pairs_hook(args):
        results.append(("object_pairs_hook", list(args)))
        return dict(args)

    callbacks = {k: v for k, v in locals().items() if '_' in k}

    return loads(text, **callbacks), results


def load_all(text, expected=None):
    j, callbacks_j = loads(json.loads, text)
    k, callbacks_k = loads(kson.loads, text)
    j2 = json.loads(text)
    k2 = kson.loads(text)

    assert j == k == j2 == k2
    assert callbacks_j == callbacks_k
    if expected is not None:
        assert callbacks_k == expected


class LoadTest(unittest.TestCase):
    def test_simple_load(self):
        expected = [('parse_int', '0')]
        load_all('0', expected)

    def test_dict(self):
        load_all('{}')

    def test_list(self):
        load_all('[]')

    def test_dict1(self):
        load_all('{"foo": "bar"}')

    def test_dict2(self):
        load_all('{"foo": "bar", "bar": 3}')

    def test_dict3(self):
        load_all('{"foo": {"bar": 3}}')

    def test_dict4(self):
        load_all('{"foo": {"bar": 3.3}}')

    def test_all_loading(self):
        load_all(TEST_JSON, EXPECTED2)

    def test_object(self):
        results = []

        def object_hook(*x):
            results.append(("object_hook", x))
            return x

        text = '{"one": 1, "two": {"three": false}}'
        j = json.loads(text, object_hook=object_hook)
        results_j = results[:]
        results.clear()

        k = kson.loads(text, object_hook=object_hook)
        assert j == k
        assert results_j == results

    def test_nan(self):
        text = '[NaN, Infinity, -Infinity]'
        (nan_j, *rest_j), callbacks_j = loads(json.loads, text)
        (nan_k, *rest_k), callbacks_k = loads(kson.loads, text)
        nan_j2, *rest_j2 = json.loads(text)
        nan_k2, *rest_k2 = kson.loads(text)

        assert nan_j != nan_j
        assert nan_k != nan_k
        assert nan_j2 != nan_j2
        assert nan_k2 != nan_k2
        assert rest_j == rest_k
        assert rest_k == rest_j2
        assert rest_j2 == rest_k2
        assert callbacks_j == callbacks_k

    def test_stream(self):
        fp = io.StringIO('[1, 2, 3]')
        assert kson.load(fp) == [1, 2, 3]


EXPECTED = [
    ('object_pairs_hook', []),
    ('object_pairs_hook', [('YES', True), ('NO', False)]),
    ('parse_int', '0'),
    ('parse_int', '1'),
    ('parse_int', '-2'),
    ('parse_float', '3.3'),
    ('parse_float', '4.4e5'),
    ('parse_float', '6.6e-7'),
    (
        'object_pairs_hook',
        [
            ('empty_object', {}),
            ('empty_array', []),
            ('booleans', {'YES': True, 'NO': False}),
            ('numbers', [0, 1, -2, 3.3, 440000.0, 6.6e-07]),
            ('strings', ['This', ['And', 'That', 'And a "b']]),
            ('nothing', None),
        ],
    ),
]

EXPECTED2 = [
    ('object_pairs_hook', []),
    ('object_pairs_hook', [('YES', True), ('NO', False)]),
    ('parse_int', '0'),
    ('parse_int', '1'),
    ('parse_int', '-2'),
    ('parse_float', '3.3'),
    ('parse_float', '4.4e5'),
    ('parse_float', '6.6e-7'),
    ('object_pairs_hook', [
        ('empty_object', {}),
        ('empty_array', []),
        ('booleans', {'NO': False, 'YES': True}),
        ('numbers', [0, 1, -2, 3.3, 440000.0, 6.6e-07]),
        ('strings', ['This', ['And', 'That', 'And a "b']]),
        ('nothing', None)
    ])
]
