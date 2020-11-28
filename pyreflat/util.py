from .core import DictTokenizer
from .interp import DictIterpreter
from .flatter import FlatWriter, FlatReader
from .conv import Convert


class FileAlreadyOpenError(Exception):
    pass


class FlatFile(object):
    def __init__(self, fnam, mode="r", converter=Convert):
        self._fnam = fnam
        self._mode = mode
        self._fd = None
        self._convert = converter

    def open(self):
        if self._fd:
            raise FileAlreadyOpenError()
        self._fd = open(self._fnam, self._mode)

    def close(self):
        if self._fd:
            self._fd.close()
            self._fd = None

    def write(self, dic, write_nl=False):
        toknizr = DictTokenizer(emitType=True, converter=self._convert)
        toknizr.from_dict(dic)
        writer = FlatWriter(toknizr, write_nl=write_nl)
        writer.write(file=self._fd)

    def read(self):
        content = self._fd.read()
        reader = FlatReader()
        ipret = DictIterpreter(converter=self._convert)
        ipret.run_all(reader.emit_from(content))
        return ipret.result()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, t, v, tb):
        self.close()
