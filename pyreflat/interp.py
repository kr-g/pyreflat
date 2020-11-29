from .conv import Convert
from .tokens import Key, Index, SetIndex, TupleIndex, TerminalValueType, TerminalValue


class Command(object):
    def __init__(self, interp, token):
        self.interp = interp
        self.token = token

    def _get_conv(self):
        return self.interp._converter()

    def run(self, env):
        raise NotImplementedError


class TerminalValueCmd(Command):
    def run(self, env):
        return self.token.val


class TerminalValueTypeCmd(Command):
    def run(self, env):

        cmd = self.interp._pop()
        env = cmd.run(env)

        if self.token.val == "str":
            env = self._get_conv().decode(str(env))
            return env

        env = env.strip()

        if self.token.val == "int":
            env = int(env)
        elif self.token.val == "float":
            env = float(env)
        elif self.token.val == "bool":
            env = env.lower() == "true"
        elif self.token.val == "complex":
            env = complex(env)

        return env


class IndexCmd(Command):
    def run(self, env):

        if type(env) != list:
            env = list(env)

        idx = self.token.val
        env.extend([None for i in range(0, idx + 1 - len(env))])

        cmd = self.interp._pop()
        env[idx] = cmd.run(env[idx] or {})

        return env


class SetIndexCmd(IndexCmd):
    def run(self, env):
        env = super().run(env)
        env = set(env)
        return env


class TupleIndexCmd(IndexCmd):
    def run(self, env):
        env = super().run(env)
        env = tuple(env)
        return env


class KeyCmd(Command):
    def run(self, env):
        key = self.token.val

        if key not in env:
            env[key] = {}

        cmd = self.interp._pop()
        env[key] = cmd.run(env[key])

        return env


class DictIterpreter(object):
    def __init__(self, converter=Convert):
        self.reset()
        self._stack = list()
        self._map = {}
        self._converter = converter
        self._set_defaults()

    def _set_defaults(self):
        self.set_command(Key, KeyCmd)
        self.set_command(TerminalValue, TerminalValueCmd)
        self.set_command(TerminalValueType, TerminalValueTypeCmd)
        self.set_command(Index, IndexCmd)
        self.set_command(TupleIndex, TupleIndexCmd)
        self.set_command(SetIndex, SetIndexCmd)

    def set_command(self, tokenType, cmd):
        self._map[tokenType] = cmd

    def __repr__(self):
        return str(self._dic)

    def _push(self, token):
        self._stack.append(token)

    def _pop(self):
        return self._stack.pop(0)

    def run(self, token):
        tt = type(token)
        if tt not in self._map:
            print("missing token, skip processing for", token)
            return

        cmd = self._map[tt](self, token)
        self._push(cmd)

        if not isinstance(token, TerminalValue):
            return

        cmd = self._pop()
        cmd.run(self._dic)

    def run_all(self, it):
        for token in it:
            self.run(token)

    def result(self):
        return self._dic

    def reset(self):
        self._dic = {}
