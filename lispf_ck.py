import ox
import click
import pprint
import sys
from sys import stdin

lexer = ox.make_lexer([
    ('NAME', r'[-a-zA-Z]+'),
    ('NUMBER', r'\d+'),
    ('PARENTESE_A', r'\('),
    ('PARENTESE_F', r'\)'),
    ('COMMENT', r';.*'),
    ('NEWLINE', r'\n'),
    ('SPACE', r'\s+')
])


tokens = ['PARENTESE_F','PARENTESE_A','NUMBER','NAME']
cellptr = 0
cells = [0]
codeptr = 0

name = lambda name: ('name', name)
number = lambda number: ('number', int(number))
op = lambda op: (op)
parser = ox.make_parser([
	('program : PARENTESE_A expr PARENTESE_F', lambda x,y,z: y),
    ('program : PARENTESE_A PARENTESE_F', lambda x,y: '()'),
	('expr : operator expr', lambda x,y: (x,) + y),
	('expr : operator', lambda x: (x,)),
	('operator : program', op),
    ('operator : NAME', name),
    ('operator : NUMBER', number),
], tokens)


def right():
    global cellptr
    cellptr += 1
    if cellptr == len(cells):
        cells.append(0)

def left():
    global cellptr
    if cellptr <= 0:
        cellptr = 0
    else:
        cellptr -= 1

def inc():
    global cellptr
    if cells[cellptr] < 255:
        cells[cellptr] = cells[cellptr] + 1
    else:
        cells[cellptr] = 0

def dec():
    global cellptr
    if cells[cellptr] > 0:
        cells[cellptr] = cells[cellptr] - 1
    else:
        cells[cellptr] = 255

def sub(number):
    while number != 0:
        dec()
        number -= 1

def loop(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap


def add(number):
    while number != 0:
        inc()
        number -= 1

def _print():
    sys.stdout.write(chr(cells[cellptr]))

def read():
    global cellptr, cells
    cells[cellptr] = ord(stdin.read(1))

OP_TO_FUNC = {
    'right': right(),    # > in brainfuck
    'left': left(),     # < in brainfuck
    'print': _print(),     # . in brainfuck
    'read': read(),     # , in brainfuck
    'loop': loop(),         # [] in brainfuck
    'inc': inc(),         # + in brainfuck
    'dec': dec(),         # - in brainfuck
}

_OP_TO_FUNC = {
    'add': add(number),  # > in brainfuck x times
    'sub': sub(number),     # < in brainfuck x times
}

def eval(ast):
    head, *tail = ast
    if isinstance(head, int):
        return tail[0]
    elif head in OP_TO_FUNC:
        OP_TO_FUNC[head]()
        return
    elif head in _OP_TO_FUNC:
        func = _OP_TO_FUNC[head]
        x = map(eval, tail)
        return func(x)
    else:
        raise ValueError('operador invalido: %s' % head)


@click.command()
@click.argument('source', type=click.File('r'))
def make_tree(source):
    program = source.read()
    print('program: ', program)
    tokens = lexer(program)

    # removing space and comment tokens before passing list to parser
    parser_tokens = [token for token in tokens if token.type != 'COMMENT' and token.type != 'SPACE']

    tree = parser(parser_tokens)
    return tree

if __name__ == '__main__':
    tree = make_tree()
    print('\n\ntree:', tree) # Abstract syntax tree
    #eval(tree)
