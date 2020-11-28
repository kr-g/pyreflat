import os
import tempfile
import unittest

from pyreflat import FlatFile


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


class Flatten_File_TestCase(unittest.TestCase):
    def test_1(self):

        temp_path = tempfile.gettempdir()
        temp_fnam = tempfile.gettempprefix() + "_flat_test.txt"
        fnam = os.path.join(temp_path, temp_fnam)

        print("fnam=", fnam)

        with FlatFile(fnam, "w") as f:
            f.write(test_dict)

        with FlatFile(fnam) as f:
            dic = f.read()

        os.remove(fnam)

        self.assertEqual(test_dict, dic)
        del dic["a"]

        self.assertNotEqual(test_dict, dic)
