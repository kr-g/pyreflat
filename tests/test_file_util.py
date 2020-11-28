import os
import tempfile
import unittest

from pyreflat import FlatFile
from pyreflat.conv import Convert, ConvertHex, ConvertUTF8


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


class Flatten_File_TestCase(unittest.TestCase):
    def setUp(self):
        print("start")
        self.dic_data = get_test_data()

    def tearDown(self):
        print("down")

    def test_1(self):

        temp_path = tempfile.gettempdir()
        temp_fnam = tempfile.gettempprefix() + "_flat_test.txt"
        fnam = os.path.join(temp_path, temp_fnam)

        print("fnam=", fnam)

        test_dict = self.dic_data

        with FlatFile(fnam, "w") as f:
            f.write(test_dict)

        with FlatFile(fnam) as f:
            dic = f.read()

        os.remove(fnam)

        self.assertEqual(test_dict, dic)
        del dic["a"]

        self.assertNotEqual(test_dict, dic)

    def test_2(self):

        temp_path = tempfile.gettempdir()
        temp_fnam = tempfile.gettempprefix() + "_flat_test.txt"
        fnam = os.path.join(temp_path, temp_fnam)

        print("fnam=", fnam)

        test_dict = self.dic_data

        with FlatFile(fnam, "w", converter=ConvertHex) as f:
            f.write(test_dict)

        with FlatFile(fnam, converter=ConvertHex) as f:
            dic = f.read()

        print(dic)
        os.remove(fnam)

        self.maxDiff = None

        self.assertEqual(test_dict, dic)
        del dic["a"]

        self.assertNotEqual(test_dict, dic)

    def test_3(self):

        temp_path = tempfile.gettempdir()
        temp_fnam = tempfile.gettempprefix() + "_flat_test.txt"
        fnam = os.path.join(temp_path, temp_fnam)

        print("fnam=", fnam)

        test_dict = self.dic_data

        with FlatFile(fnam, "w", converter=ConvertUTF8) as f:
            f.write(test_dict)

        with FlatFile(fnam, converter=ConvertUTF8) as f:
            dic = f.read()

        print(dic)
        # os.remove(fnam)

        self.maxDiff = None

        self.assertEqual(test_dict, dic)
        del dic["a"]

        self.assertNotEqual(test_dict, dic)
