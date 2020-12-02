import sys

from .tokens import Key, Index, SetIndex, TupleIndex, TerminalValueType, TerminalValue


class TabFlatWriter(object):
    def __init__(self, flatdict, write_nl=True):
        self._flt = flatdict
        # for compatibility,
        # ##todo rework interface
        self._write_nl = write_nl

    def write(self, file=sys.stdout):

        for tokens in self._flt:
            path, val = tokens
            for pr in path:
                file.write(pr.__class__.__name__)
                file.write(":")
                file.write(str(pr.val))
                file.write("\t")
            file.write(val.__class__.__name__)
            file.write(":")
            file.write(str(val.val))
            file.write("\n")


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
