from .tokens import Key, Index, SetIndex, TupleIndex, TerminalValueType, TerminalValue


class DictTokenizer(object):
    def __init__(self, emitType=True):
        self._dic = {}
        self.emitType = emitType

    def from_dict(self, dic):
        self._dic = dic

    def __iter__(self):
        el = []
        stack = list()
        for t in self._it(self._dic, stack):
            if isinstance(t, TerminalValue):
                yield list(el), t
                el.clear()
            else:
                el.append(t)
        if len(stack) > 0:
            raise Exception("malformed syntax")

    def _it(self, el, stack):
        for key, val in el.items():
            stack.append(Key(key))
            if type(val) == dict:
                yield from self._it(val, stack)
            elif type(val) in [list, set, tuple]:
                yield from self._it_list(val, stack)
            else:
                yield from stack
                if self.emitType:
                    yield TerminalValueType(val.__class__.__name__)
                yield TerminalValue(val)
            stack.pop()

    def _it_list(self, el, stack):
        for i, val in enumerate(el):

            if type(el) == list:
                stack.append(Index(i))
            elif type(el) == set:
                stack.append(SetIndex(i))
            elif type(el) == tuple:
                stack.append(TupleIndex(i))

            if type(val) == dict:
                yield from self._it(val, stack)
            elif type(val) in [list, set, tuple]:
                yield from self._it_list(val, stack)
            else:
                yield from stack
                if self.emitType:
                    yield TerminalValueType(val.__class__.__name__)
                yield TerminalValue(val)
            stack.pop()
