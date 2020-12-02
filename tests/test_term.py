import io

import json

from pyreflat import DictTokenizer, TerminalWriter


import unittest


test_dict = {
    "a": 1,
    "b": 2.1,
    "c": "hello world",
    "d": {
        "z": 100,
        "y": 100.0,
        "x": "sub dict",
    },
    "e": [1, 3, 5, 7],
    "f": {
        "w": 200,
        "v": 200.0,
        "u": "sub dict 2",
        "fu": [11, 13, 17, {"fua": 153}, 19],
    },
    "g": [{"ga": 3000}, 1, [1, 2, 3, 4]],
    "h": [[1], [2, [2.1]], [3, [3.1, [3.2, 3.3, {"deep": True, "deeper": False}, -1]]]],
    "i": set([100, 300, 500, 700]),
    "j": tuple([1000, 3000, 5000, 7000]),
    "cplx": complex(1.1, 2.2),
    "lastentry": False,
    "done": True,
}

TOTAL_TERMINAL_VALUES_IN_SAMPLE = 45


class Flatten_TestCase(unittest.TestCase):
    def test_null_list(self):

        toknizr = DictTokenizer()
        toknizr.from_dict(test_dict)

        trmwr = TerminalWriter(toknizr)

        terminal_values = trmwr.write()

        print("terminal_values", terminal_values)

        # numbers of terminal values in the example abode
        self.assertEqual(len(terminal_values), TOTAL_TERMINAL_VALUES_IN_SAMPLE)

    def test_with_list_provided(self):

        toknizr = DictTokenizer()
        toknizr.from_dict(test_dict)

        trmwr = TerminalWriter(toknizr)

        terminal_values = list()
        rc = trmwr.write(terminal_values)

        self.assertEqual(terminal_values, rc)

        # numbers of terminal values in the example abode
        self.assertEqual(len(terminal_values), TOTAL_TERMINAL_VALUES_IN_SAMPLE)
