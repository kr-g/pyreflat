import io

import json

from pyreflat import DictTokenizer, DictIterpreter, FlatWriter, FlatReader


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


class Flatten_TestCase(unittest.TestCase):
    def test_1(self):

        toknizr = DictTokenizer(emitType=True)
        toknizr.from_dict(test_dict)

        fltwr = FlatWriter(toknizr, write_nl=True)

        buf = io.StringIO()
        fltwr.write(file=buf)

        content = buf.getvalue()

        fltrd = FlatReader()
        ipret = DictIterpreter()

        ipret.run_all(fltrd.emit_from_i(content.splitlines()))

        r = ipret.result()

        self.assertEqual(r.get("a"), 1)
        self.assertNotEqual(r.get("a"), "1")
        self.assertEqual(type(r.get("a")), int)

        self.assertEqual(r.get("b"), 2.1)
        self.assertNotEqual(r.get("b"), "2.1")
        self.assertEqual(type(r.get("b")), float)

        self.assertEqual(r.get("c"), "hello world")
        self.assertEqual(type(r.get("c")), str)

        self.assertEqual(r.get("cplx"), complex(1.1, 2.2))
        self.assertEqual(r.get("i"), set([100, 300, 500, 700]))
        self.assertEqual(r.get("j"), tuple([1000, 3000, 5000, 7000]))

        self.assertEqual(
            r.get("h"),
            [
                [1],
                [2, [2.1]],
                [3, [3.1, [3.2, 3.3, {"deep": True, "deeper": False}, -1]]],
            ],
        )
