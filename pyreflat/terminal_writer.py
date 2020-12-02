from .tokens import TerminalValue
from .core import MalformedSyntaxError


class TerminalWriter(object):
    def __init__(self, flatdict):
        self._flt = flatdict

    def write(self, output=None):

        if output == None:
            output = list()

        for tokens in self._flt:
            path, terminal = tokens
            if type(terminal) != TerminalValue:
                raise MalformedSyntaxError()
            output.append(terminal.val)

        return output
