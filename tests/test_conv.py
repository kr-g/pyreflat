import unittest

from pyreflat.conv import Convert, ConvertHex, ConvertUTF8


test_data = "hello\tworld\n"


class Converter_TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def __convert_test(self, conv):
        a = conv().encode(test_data)
        b = str(a)
        c = conv().decode(b)
        self.assertEqual(test_data, c)

    def test_Convert(self):
        self.__convert_test(Convert)

    def test_ConvertHex(self):
        self.__convert_test(ConvertHex)

    def test_ConvertUTF8(self):
        self.__convert_test(ConvertUTF8)
