from .core import DictTokenizer
from .interp import DictIterpreter
from .flatter import FlatWriter, FlatReader
from .tab_flat import TabFlatWriter, TabFlatReader
from .conv import ConvertUTF8


class FileAlreadyOpenError(Exception):
    pass


class FlatFile(object):
    def __init__(self, fnam, mode="r", converter=ConvertUTF8):
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

    def write(self, dic, write_nl=True, writer=FlatWriter):
        toknizr = DictTokenizer(converter=self._convert)
        toknizr.from_dict(dic)
        wrt = writer(toknizr, write_nl=write_nl)
        wrt.write(file=self._fd)

    def read(self, split_lines=True, reader=FlatReader):
        content = self._fd.read()
        rdr = reader()
        ipret = DictIterpreter(converter=self._convert)
        if split_lines:
            content = content.splitlines()
            ipret.run_all(rdr.emit_from_i(content))
        else:
            ipret.run_all(rdr.emit_from(content))
        return ipret.result()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, t, v, tb):
        self.close()
