from .test_round_trip import TEST_JSON
from kson.read import load
import json
import math
import unittest


def loads_callbacks(loads, text):
    results = []

    def object_hook(x):
        results.append(("object_hook", x))
        return x

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
            return math.inf
        raise ValueError("%s" % x)

    def object_pairs_hook(args):
        results.append(("object_pairs_hook", args))
        return dict(args)

    callbacks = {k: v for k, v in locals().items() if '_' in k}

    return loads(text, **callbacks), results


def load_all_callbacks(text, expected=None):
    KSON_CALLBACKS_WORK = not False

    j1, callbacks1 = loads_callbacks(json.loads, text)
    if KSON_CALLBACKS_WORK:
        j2, callbacks2 = loads_callbacks(load.loads, text)
    else:
        j2, callbacks2 = j1, callbacks1
    j3 = json.loads(text)
    j4 = load.loads(text)

    assert j1 == j2 == j3 == j4
    if expected is not None:
        assert callbacks1 == callbacks2 == expected


class LoadTest(unittest.TestCase):
    def test_simple_load(self):
        expected = [('parse_int', '0')]
        load_all_callbacks('0', expected)

    def test_dict(self):
        load_all_callbacks('{}')

    def test_list(self):
        load_all_callbacks('[]')

    def test_dict2(self):
        load_all_callbacks('{"foo": "bar"}')

    def NO_test_all(self):
        load_all_callbacks(TEST_JSON, EXPECTED)


TEST_JSON2 = """{}"""


EXPECTED = [
    ("object_pairs_hook", []),
    ("object_pairs_hook", [("YES", True), ("NO", False)]),
    ("parse_int", "0"),
    ("parse_int", "1"),
    ("parse_int", "-2"),
    ("parse_float", "3.3"),
    ("parse_float", "4.4e5"),
    ("parse_float", "6.6e-7"),
    (
        "object_pairs_hook",
        [
            ("empty_object", {}),
            ("empty_array", []),
            ("booleans", {"YES": True, "NO": False}),
            ("numbers", [0, 1, -2, 3.3, 440000.0, 6.6e-07]),
            ("strings", ["This", ["And", "That", 'And a "b']]),
            ("nothing", None),
        ],
    ),
]
