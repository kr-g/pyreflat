import io
import json
import bisect

from pyreflat import DictTokenizer, AnynomusPathWriter


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


class Any_Path_base_TestCase(unittest.TestCase):
    def test_writer(self):

        toknizr = DictTokenizer()
        toknizr.from_dict(test_dict)

        trmwr = AnynomusPathWriter(toknizr)

        path_val = trmwr.write()
        self.assertEqual(len(path_val), TOTAL_TERMINAL_VALUES_IN_SAMPLE)


class Any_Path_TestCase(unittest.TestCase):
    def setUp(self):

        toknizr = DictTokenizer()
        toknizr.from_dict(test_dict)

        trmwr = AnynomusPathWriter(toknizr)

        self.path_val = trmwr.write()

    def tearDown(self):
        self.path_val = None

    def test_search_all_1(self):

        path_val = self.path_val

        # search in all
        el = list(filter(lambda x: x[0].find("deep") >= 0, path_val))

        self.assertTrue(len(el) == 2)

    def test_search_all_2(self):

        path_val = self.path_val

        # search in all
        # base is key "g" from the dict, followed by 2 list levels marked as "__l"
        search_for = "g__l__l"
        el_found = filter(lambda x: x[0] == search_for, path_val)
        el = list(map(lambda x: x[1], el_found))

        self.assertTrue(len(el) == 4)

    def test_search_sorted(self):

        path_val = self.path_val

        # sort result by path
        path_val = sorted(path_val, key=lambda x: x[0])

        # unzip key and val with keeping both in order
        keys, vals = list(zip(*path_val))

        print("keys", keys)
        print("vals", vals)

        # search in sorted
        # base is key "g" from the dict, followed by 2 list levels marked as "__l"
        search_for = "g__l__l"
        idx = bisect.bisect_left(keys, search_for)
        found = []
        while idx < len(keys):
            if keys[idx] == search_for:
                found.append(vals[idx])
                idx += 1
            else:
                break

        self.assertTrue(len(found) == 4)
