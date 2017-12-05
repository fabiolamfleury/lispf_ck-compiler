import ox
import click

from interpreter import Interpreter


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

name = lambda name: (name)
number = lambda number: (int(number))
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


@click.command()
@click.argument('source', type=click.File('r'))
@click.option('-o', nargs=1, type=click.File('w'))
def make_tree(source, o):
    program = source.read()
    print('program: ', program)
    tokens = lexer(program)

    # removing space and comment tokens before passing list to parser
    parser_tokens = [token for token in tokens if token.type != 'COMMENT' and token.type != 'SPACE']

    tree = parser(parser_tokens)
    interpreter = Interpreter()
    interpreter.eval(tree)
    brainf = interpreter.result()
    print('Brainfuck translation: \n', brainf)
    print('\n')
    print('Program ', o.name, 'saved')
    o.write(brainf)
    o.flush()

if __name__ == '__main__':
    tree = make_tree()
