from .tokens import Key, Index, SetIndex, TupleIndex, TerminalValue


class Writer(object):
    def __init__(self, subst=None, add_not_empty=None):
        self._subst = subst
        self._add_not_empty = add_not_empty

    def write(self, token, output):
        if self._subst:
            output += str(self._subst)
        else:
            if len(output) > 0 and self._add_not_empty:
                output += self._add_not_empty
            output += str(token.val)
        return output


class AnynomusPathWriter(object):
    def __init__(self, flatdict, base=Writer):
        self._flt = flatdict
        self._map = {}
        self._base = base
        self._set_defaults()

    def _set_defaults(self):
        self.set_writer(Key, self._base(add_not_empty="_"))
        self.set_writer(TerminalValue, self._base())

        self.set_writer(Index, self._base("__l"))
        self.set_writer(SetIndex, self._base("__s"))
        self.set_writer(TupleIndex, self._base("__t"))

    def set_writer(self, token_type, writer):
        self._map[token_type] = writer

    def write(self, output=None):

        if output == None:
            output = list()

        for tokens in self._flt:
            cur = ""
            path, val = tokens
            for pr in path:
                if type(pr) in self._map:
                    cur = self._map[type(pr)].write(pr, cur)
                else:
                    pass

            output.append((cur, val.val))

        return output
