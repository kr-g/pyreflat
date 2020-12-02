from .conv import ConvertUTF8
from .tokens import Key, Index, SetIndex, TupleIndex, TerminalValueType, TerminalValue


class MalformedSyntaxError(Exception):
    pass


class DictTokenizer(object):
    def __init__(self, converter=ConvertUTF8):
        self._dic = {}
        self._converter = converter

    def from_dict(self, dic):
        self._dic = dic

    def __iter__(self):
        el = []
        stack = list()

        for token in self._it(self._dic, stack):
            if isinstance(token, TerminalValue):
                yield list(el), token
                el.clear()
            else:
                el.append(token)

        if len(stack) > 0:
            raise MalformedSyntaxError()

    def _it(self, el, stack):
        for key, val in el.items():

            stack.append(Key(key))

            typ_val = type(val)
            if typ_val == dict:
                yield from self._it(val, stack)
            elif typ_val in [list, set, tuple]:
                yield from self._it_list(val, stack)
            else:
                yield from self._y_terminal(stack, val)

            stack.pop()

    def _y_terminal(self, stack, val):
        yield from stack
        yield TerminalValueType(val.__class__.__name__)
        if type(val) == str:
            yield TerminalValue(self._converter().encode(str(val)))
        else:
            yield TerminalValue(val)

    def _it_list(self, el, stack):
        for i, val in enumerate(el):

            typ_el = type(el)
            if typ_el == list:
                stack.append(Index(i))
            elif typ_el == set:
                stack.append(SetIndex(i))
            elif typ_el == tuple:
                stack.append(TupleIndex(i))

            typ_val = type(val)
            if typ_val == dict:
                yield from self._it(val, stack)
            elif typ_val in [list, set, tuple]:
                yield from self._it_list(val, stack)
            else:
                yield from self._y_terminal(stack, val)

            stack.pop()
