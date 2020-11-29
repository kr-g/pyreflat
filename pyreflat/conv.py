class ConverterBase(object):
    def __init__(self):
        pass

    def encode(self, astr):
        raise NotImplementedError

    def decode(self, astr):
        raise NotImplementedError


class Convert(ConverterBase):
    def encode(self, astr):
        return astr

    def decode(self, astr):
        return astr


class ConvertUTF8(ConverterBase):
    def encode(self, astr):
        return astr.encode("unicode-escape").decode()

    def decode(self, astr):
        return astr.encode().decode("unicode-escape")


class ConvertHex(ConverterBase):
    def encode(self, astr):
        return astr.encode().hex()

    def decode(self, astr):
        return bytes.fromhex(astr).decode()
