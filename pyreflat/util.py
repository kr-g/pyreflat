from .core import DictTokenizer
from .interp import DictIterpreter
from .flatter import FlatWriter, FlatReader


class FileAlreadyOpenError(Exception):
    pass


class FlatFile(object):
    def __init__(self, fnam, mode="r"):
        self._fnam = fnam
        self._mode = mode
        self._fd = None

    def open(self):
        if self._fd:
            raise FileAlreadyOpenError()
        self._fd = open(self._fnam, self._mode)

    def close(self):
        if self._fd:
            self._fd.close()
            self._fd = None

    def write(self, dic):
        toknizr = DictTokenizer(emitType=True)
        toknizr.from_dict(dic)
        writer = FlatWriter(toknizr)
        writer.write(file=self._fd)

    def read(self):
        content = self._fd.read()
        reader = FlatReader()
        ipret = DictIterpreter()
        ipret.run_all(reader.emit_from_i(content.splitlines()))
        return ipret.result()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, t, v, tb):
        self.close()
