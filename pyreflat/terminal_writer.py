from .tokens import TerminalValue


class TerminalWriter(object):
    def __init__(self, flatdict):
        self._flt = flatdict

    def write(self, output=None):

        if output == None:
            output = list()

        for tokens in self._flt:
            path, terminal = tokens
            output.append(terminal.val)

        return output
