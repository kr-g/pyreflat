import sys

from .tokens import Key, Index, SetIndex, TupleIndex, TerminalValueType, TerminalValue
from pyreflat.conv import ConvertUTF8


class TabFlatWriter(object):
    def __init__(self, flatdict, write_nl=True):
        self._flt = flatdict
        self._fd = sys.stdout
        self._map = {}
        # self._write_nl = write_nl

    def set_writer(self, token_type, writer):
        self._map[token_type] = writer

    def write(self, file=sys.stdout):
        self._fd = file

        for tokens in self._flt:
            path, val = tokens
            for pr in path:
                self._fd.write(pr.__class__.__name__)
                self._fd.write(":")
                self._fd.write(str(pr.val))
                self._fd.write("\t")
            self._fd.write(val.__class__.__name__)
            self._fd.write(":")
            self._fd.write(str(val.val))
            self._fd.write("\n")


class TabReader(object):
    def __init__(self, token_type):
        self._type = token_type
        self._nam = token_type.__name__


class TabFlatReader(object):
    def __init__(self):
        self._map = {}
        self._set_defaults()

    def _set_defaults(self):
        self.set_reader(TabReader(Key))
        self.set_reader(TabReader(Index))
        self.set_reader(TabReader(SetIndex))
        self.set_reader(TabReader(TupleIndex))
        self.set_reader(TabReader(TerminalValue))
        self.set_reader(TabReader(TerminalValueType))

    def set_reader(self, reader):
        self._map[reader._nam] = reader

    def emit_from(self, line):
        while len(line) > 0:
            found = False
            fields = line.split("\t")
            for fld in fields:
                tok_val = fld.split(":")
                if len(tok_val) != 2:
                    raise Exception("malformed token", line[0:10] + "...")
                tok, val = tok_val
                if tok not in self._map:
                    raise Exception("unknown token", line[0:10] + "...")
                token = self._map[tok]._type(val)
                yield token
            line = ""

    def emit_from_i(self, content):
        for line in content:
            yield from self.emit_from(line)
