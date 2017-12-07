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
        self.functions_with_args = {}

    def define(self, code):
        if code[1] == '()':
            self.functions[code[0]] = code[2]
        else:
            self.functions_with_args[code[0]] = [code[2], code[1]]

    def func_with_args(self, head, tail):
        """
            head[0] # code
            head[1] # args tuple
            tail # passed args
        """
        count = 0
        print(type(head[0]))
        for element in head[1]:
            aux_lst = list(head[0])
            for index, item in enumerate(aux_lst):
                if isinstance(item, str) and element is item:
                    aux_lst[index] = tail[count]
                    head[0] = tuple(aux_lst)
                elif not isinstance(item, str) and not isinstance(item, int):
                    print('\n',item)
                    new_head = [item, head[1]]
                    aux_lst[index] = self.func_with_args(new_head, tail)
                    print('\n\n\nEOQ', aux_lst[index], aux_lst)
            count = count + 1
            head[0] = tuple(aux_lst)
        print(head ,'head1',head[1], 'tail',tail, 'head 0',head[0])
        return head[0]

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
        elif head in self.functions_with_args:
            func_args = self.func_with_args(self.functions_with_args[head], tail)
            print('\n\n\fun_args', func_args)
            return self.do(func_args)
        else:
            raise ValueError('operador invalido: %s' % head)
