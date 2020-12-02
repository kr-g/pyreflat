import io

import json

from pyreflat import DictTokenizer, DictIterpreter, FlatWriter, FlatReader
from pyreflat.flatter import (
    KEY_ID,
    INDEX_ID,
    SET_INDEX_ID,
    TUPLE_INDEX_ID,
    TERMINAL_VALUE_TYPE_ID,
    TERMINAL_VALUE_ID,
)


import unittest


T1V = "hello" + KEY_ID + "world"
T2V = "hello" + INDEX_ID + "world"
T3V = "hello" + SET_INDEX_ID + "world"
T4V = "hello" + TUPLE_INDEX_ID + "world"
T5V = "hello" + TERMINAL_VALUE_TYPE_ID + "world"
T6V = "hello" + TERMINAL_VALUE_ID + "world"


test_dict = {
    "a": 1,
    "b": 2.1,
    "c1": T1V,
    "c2": T2V,
    "c3": T3V,
    "c4": T4V,
    "c5": T5V,
    "c6": T6V,
    "d": {
        "z": 100,
        "y": 100.0,
        "x": "sub dict",
    },
}


class Chars_TestCase(unittest.TestCase):
    def test_1(self):

        toknizr = DictTokenizer()
        toknizr.from_dict(test_dict)

        fltwr = FlatWriter(toknizr, write_nl=True)

        buf = io.StringIO()
        fltwr.write(file=buf)

        content = buf.getvalue()

        print("escaped", content)

        fltrd = FlatReader()
        ipret = DictIterpreter()

        ipret.run_all(fltrd.emit_from_i(content.splitlines()))

        r = ipret.result()

        val = r["c1"]
        print("got", val)
        self.assertTrue(val == T1V)

        val = r["c2"]
        print("got", val)
        self.assertTrue(val == T2V)

        val = r["c3"]
        print("got", val)
        self.assertTrue(val == T3V)

        val = r["c4"]
        print("got", val)
        self.assertTrue(val == T4V)

        val = r["c5"]
        print("got", val)
        self.assertTrue(val == T5V)

        val = r["c6"]
        print("got", val)
        self.assertTrue(val == T6V)
