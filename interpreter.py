from sys import stdin

class Interpreter():
    def __init__(self):
        self.string = ''

        self.OP_TO_FUNC = {
            'right': '>',    # > in brainfuck
            'left': '<',     # < in brainfuck
            'print': '.',     # . in brainfuck
            'read': ',',     # , in brainfuck
            'inc': '+',         # + in brainfuck
            'dec': '-',         # - in brainfuck
        }

        self._OP_TO_FUNC = {
            'add': self.add,  # > in brainfuck x times
            'sub': self.sub,     # < in brainfuck x times
            'do': self.do,
            'loop': self.loop,         # [] in brainfuck
            'do-before': self.do_before,
            'do-after': self.do_after,
            'def': self.define,
        }
        self.functions = {}

    def define(self, code):
        self.functions[code[0]] = code[2]

    def result(self):
        return self.string

    def add(self, number):
        increment = number[0]
        while increment != 0:
            self.string += '+'
            increment = increment - 1

    def sub(self, number):
        increment = number[0]
        while increment != 0:
            self.string += '-'
            increment = increment - 1

    def loop(self, code):
        self.string += '['
        self.do(code)
        self.string += ']'

    def do(self, code):
        for operation in code:
            if isinstance(operation, str):
                if operation in self.OP_TO_FUNC:
                    self.string += self.OP_TO_FUNC[operation]
                elif operation in self._OP_TO_FUNC:
                    func = self._OP_TO_FUNC[operation]
                    func()
                elif operation in self.functions:
                    self.eval(self.functions[operation])
            else:
                self.eval(operation)

    def do_before(self,code):
        before_command, command_list = code
        new_code = ['do']
        for command in command_list:
            new_code.extend([before_command, command])
        self.eval(new_code)

    def do_after(self,code):
        after_command, command_list = code
        new_code = ['do']
        for command in command_list:
            new_code.extend([command, after_command])
        self.eval(new_code)

    def eval(self, ast):
        head, *tail = ast

        if head in self.OP_TO_FUNC:
            self.string += self.OP_TO_FUNC[head]
            return
        elif head in self._OP_TO_FUNC:
            func = self._OP_TO_FUNC[head]
            return func(tail)
        elif isinstance(head, int):
            return tail[0]
        elif head in self.functions:
            self.eval(self.functions[head])
        else:
            raise ValueError('operador invalido: %s' % head)
