import sys
from sys import stdin

class Interpreter():
    def __init__(self):
        self.cellptr = 0
        self.cells = [0]
        self.codeptr = 0

        self.OP_TO_FUNC = {
            'right': self.right,    # > in brainfuck
            'left': self.left,     # < in brainfuck
            'print': self._print,     # . in brainfuck
            'read': self.read,     # , in brainfuck
            'inc': self.inc,         # + in brainfuck
            'dec': self.dec,         # - in brainfuck
        }

        self._OP_TO_FUNC = {
            'add': self.add,  # > in brainfuck x times
            'sub': self.sub,     # < in brainfuck x times
            'do': self.do,
            'loop': self.loop,         # [] in brainfuck
            'do-before': self.do_before,
            'do-after': self.do_after,
        }

    def right(self):
        self.cellptr += 1
        if self.cellptr == len(self.cells):
            self.cells.append(0)

    def left(self):
        if self.cellptr <= 0:
            self.cellptr = 0
        else:
            self.cellptr -= 1

    def inc(self):
        if self.cells[self.cellptr] < 255:
            self.cells[self.cellptr] = self.cells[self.cellptr] + 1
        else:
            self.cells[self.cellptr] = 0

    def dec(self):
        if self.cells[self.cellptr] > 0:
            self.cells[self.cellptr] = self.cells[self.cellptr] - 1
        else:
            self.cells[self.cellptr] = 255

    def sub(self, number):
        increment = number[0]
        while increment != 0:
            self.dec()
            increment = increment - 1

    def loop(self, code):
      while(self.cells[self.cellptr]):
            self.do(code)

    def add(self, number):
        increment = number[0]
        while increment != 0:
            self.inc()
            increment = increment - 1

    def _print(self):
        sys.stdout.write(chr(self.cells[self.cellptr]))

    def read(self):
        var = input('Input: ')
        print(int(var) % 256)
        self.cells[self.cellptr] = int(var) % 256

    def do(self, code):
        for operation in code:
            if isinstance(operation, str):
                if operation in self.OP_TO_FUNC:
                    func = self.OP_TO_FUNC[operation]
                    func()
                else:
                    func = self._OP_TO_FUNC[operation]
                    func()
            else:
                self.eval(operation)

    def do_before(self,code):
        return

    def do_after(self,code):
        return

    def eval(self, ast):
        head, *tail = ast

        if head in self.OP_TO_FUNC:
            self.OP_TO_FUNC[head]()
            return
        elif head in self._OP_TO_FUNC:
            func = self._OP_TO_FUNC[head]
            return func(tail)
        elif isinstance(head, int):
            return tail[0]
        else:
            raise ValueError('operador invalido: %s' % head)
