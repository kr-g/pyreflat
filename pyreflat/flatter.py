import sys

from .tokens import Key, Index, SetIndex, TupleIndex, TerminalValueType, TerminalValue


KEY_ID = "/"
INDEX_ID = "#"
SET_INDEX_ID = "!#"
TUPLE_INDEX_ID = "?#"
TERMINAL_VALUE_TYPE_ID = "?"
TERMINAL_VALUE_ID = "="


class Writer(object):
    def __init__(self, decor="/", end=""):
        self._decr = decor
        self._end = end

    def write(self, token, file=sys.stdout):
        print(self._decr + token.str_val(), end=self._end, file=file)


class FlatWriter(object):
    def __init__(self, flatdict, base=Writer, write_nl=True):
        self._flt = flatdict
        self._fd = sys.stdout
        self._map = {}
        self._base = base
        self._write_nl = write_nl
        self._set_defaults()

    def _set_defaults(self):
        self.set_writer(Key, self._base(KEY_ID))
        self.set_writer(Index, self._base(INDEX_ID))
        self.set_writer(SetIndex, self._base(SET_INDEX_ID))
        self.set_writer(TupleIndex, self._base(TUPLE_INDEX_ID))
        self.set_writer(TerminalValueType, self._base(TERMINAL_VALUE_TYPE_ID))
        self.set_writer(
            TerminalValue,
            self._base(TERMINAL_VALUE_ID, end=None if self._write_nl else ""),
        )

    def set_writer(self, token_type, writer):
        self._map[token_type] = writer

    def write(self, file=sys.stdout):
        self._fd = file

        for tokens in self._flt:
            path, val = tokens
            for pr in path:
                self._map[type(pr)].write(pr, file=self._fd)
            self._map[type(val)].write(val, file=self._fd)


class Reader(object):
    def __init__(self, decor, token_type):
        self._decr = decor
        self._type = token_type


class FlatReader(object):
    def __init__(self):
        self._map = {}
        self._set_defaults()

    def _set_defaults(self):
        self.set_reader(Reader(KEY_ID, Key))
        self.set_reader(Reader(INDEX_ID, Index))
        self.set_reader(Reader(SET_INDEX_ID, SetIndex))
        self.set_reader(Reader(TUPLE_INDEX_ID, TupleIndex))
        self.set_reader(Reader(TERMINAL_VALUE_ID, TerminalValue))
        self.set_reader(Reader(TERMINAL_VALUE_TYPE_ID, TerminalValueType))

    def set_reader(self, reader):
        self._map[reader._decr] = reader

    def emit_from(self, line):
        while len(line) > 0:
            found = False
            for k, trd in self._map.items():
                r = self._look_ahead(line, trd._decr)
                if r:
                    found = True
                    _, line = r
                    val, line = self._get_val(line)
                    yield trd._type(val)
                    break
            if not found:
                raise Exception("unknown token", line[0:10] + "...")

    def emit_from_i(self, content):
        for line in content:
            yield from self.emit_from(line)

    def _look_ahead(self, buf, key):
        if buf.startswith(key):
            return (True, buf[len(key) :])

    def _get_val(self, line):
        pos = 0
        while pos < len(line):
            for k, trd in self._map.items():
                if line[pos:].startswith(trd._decr):
                    return line[:pos], line[pos:]
            pos += 1
        return line, ""
