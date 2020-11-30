from .tokens import TerminalValue


class Writer(object):
    def write(self, token, output):
        output.append(token.val)


class TerminalWriter(object):
    def __init__(self, flatdict, base=Writer):
        self._flt = flatdict
        self._map = {}
        self._base = base
        self._set_defaults()

    def _set_defaults(self):
        self.set_writer(
            TerminalValue,
            self._base(),
        )

    def set_writer(self, token_type, writer):
        self._map[token_type] = writer

    def write(self, output=None):

        if output == None:
            output = list()

        for tokens in self._flt:
            path, val = tokens
            # todo refactor ?
            # for will never executed
            for pr in path:
                if type(pr) in self._map:
                    self._map[type(pr)].write(pr, output)
                else:
                    # only write terminal values out
                    pass
            # end-of todo
            self._map[type(val)].write(val, output)

        return output
