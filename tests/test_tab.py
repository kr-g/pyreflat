import os
import io
import unittest

from pyreflat import FlatFile, TabFlatWriter, TabFlatReader
from pyreflat.conv import ConvertUTF8

from pyreflat.core import DictTokenizer
from pyreflat.interp import DictIterpreter


def get_test_data():
    test_dict = {
        "a": 1,
        "b": 2.1,
        "c": "hello world",
        "c_nl": "hello\nworld\n",
        "c_nl_tab": "hello\tworld\n",
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
        "h": [
            [1],
            [2, [2.1]],
            [3, [3.1, [3.2, 3.3, {"deep": True, "deeper": False}, -1]]],
        ],
        "i": set([100, 300, 500, 700]),
        "j": tuple([1000, 3000, 5000, 7000]),
        "cplx": complex(1.1, 2.2),
        "lastentry": False,
        "done": True,
    }
    return test_dict


class TabFlatten_ReaderWriter_TestCase(unittest.TestCase):
    def setUp(self):
        print("start")
        self.dic_data = get_test_data()

    def tearDown(self):
        print("down")

    def test_tab_writer(self):

        test_dict = self.dic_data

        toknizr = DictTokenizer(converter=ConvertUTF8)
        toknizr.from_dict(test_dict)

        writer = TabFlatWriter(toknizr)

        buf = io.StringIO()
        writer.write(file=buf)

        content = buf.getvalue()
        print(content)

        reader = TabFlatReader()

        ipret = DictIterpreter(converter=ConvertUTF8)

        content = content.splitlines()
        ipret.run_all(reader.emit_from_i(content))

        res = ipret.result()

        self.maxDiff = None

        self.assertEqual(res, test_dict)
