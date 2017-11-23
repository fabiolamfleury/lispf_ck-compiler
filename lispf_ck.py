import ox
import click
import pprint

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

operator = lambda type_op: ('operator', type_op)
name = lambda name: ('name', name)
number = lambda number: ('number', int(number))
op = lambda op: (op)
opr = lambda op, num: (op, num)

parser = ox.make_parser([
	('program : PARENTESE_A expr PARENTESE_F', lambda x,y,z: y),
    ('program : PARENTESE_A PARENTESE_F', lambda x,y: '()'),
	('expr : operator expr', lambda x,y: (x,) + y),
	('expr : operator', lambda x: (x,)),
	('operator : program', op),
    ('operator : NAME', name),
    ('operator : NUMBER', number),
], tokens)

cells, codeptr, cellptr = [0], 0, 0

def right():
    cellptr += 1
    if cellptr == len(cells):
        cells.append(0)

def left():
    if cellptr <= 0:
        cellptr = 0
    else:
        cellptr -= 1

def inc():
    if cells[cellptr] < 255:
        cells[cellptr] = cells[cellptr] + 1
    else:
        cells[cellptr] = 0

def dec():
    if cells[cellptr] > 0:
        cells[cellptr] = cells[cellptr] - 1
    else:
        cells[cellptr] = 255

def sub(number):
    while number != 0:
        dec()
        number--

def add(number):
    while number != 0:
        inc()
        number

def _print():
    sys.stdout.write(chr(cells[cellptr]))

def read():
    cells[cellptr] = ord(getch.getch())

OP_TO_FUNC = {
    'right': right(),    # > in brainfuck
    'left': left(),     # < in brainfuck
    'print': lambda x, y: x * y,     # . in brainfuck
    'read': lambda x, y: x / y,     # , in brainfuck
    'add': lambda x, y: x,  # > in brainfuck x times
    'sub': lambda x: x,     # < in brainfuck x times
    'loop': lambda x: x,         # [] in brainfuck
    'inc': lambda x: x,         # + in brainfuck
    'dec': lambda x: x,         # - in brainfuck
    'def': lambda x: x,
}

def eval(ast):
    head, *tail = ast
    if head == 'atom':
        return tail[0]
    elif head in {'+', '-', '*', '/'}:
        func = OP_TO_FUNC[head]
        x, y = map(eval, tail)
        return func(x, y)
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
