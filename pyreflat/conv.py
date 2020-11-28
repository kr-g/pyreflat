import binascii


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


class ConvertHex(ConverterBase):
    def encode(self, astr):
        return astr.encode().hex()

    def decode(self, astr):
        return bytes.fromhex(astr).decode()
