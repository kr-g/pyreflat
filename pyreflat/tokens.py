class Token(object):
    def __init__(self, val, opt={}):
        self.val = val
        self.opt = opt
        self._on_init()

    def _on_init(self):
        pass

    def str_val(self):
        return str(self.val)

    def __repr__(self):
        return (
            self.__class__.__name__
            + "("
            + self.val.__class__.__name__
            + ":"
            + str(self.val)
            + ")"
        )


class TokenNumeric(Token):
    def _on_init(self):
        self.val = int(self.val)


class Key(Token):
    pass


class Index(TokenNumeric):
    pass


class TupleIndex(Index):
    pass


class SetIndex(Index):
    pass


class TerminalValue(Token):
    pass


class TerminalValueType(Token):
    pass
