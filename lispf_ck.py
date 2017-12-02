import ox
import click
import pprint
import sys
from sys import stdin

lexer = ox.make_lexer([
    ('RIGHT', r'right'), # > in brainfuck
    ('LEFT', r'left'), # < in brainfuck
    ('INC', r'inc'), # + in brainfuck
    ('DEC', r'dec'), # - in brainfuck
    ('PRINT', r'print'), # . in brainfuck
    ('READ', r'read'), # , in brainfuck
    ('DO',r'do'),
    ('ADD',r'add'),
    ('SUB',r'sub'),
    ('LOOP', r'loop'), # [] in brainfuck
    ('DEF', r'def'),
    ('NUMBER', r'\d+'),
    ('PARENTESE_A', r'\('),
    ('PARENTESE_F', r'\)'),
    ('NAME', r'[-a-zA-Z]+'),
    ('COMMENT', r';.*'),
    ('NEWLINE', r'\n'),
    ('SPACE', r'\s+')
])


tokens = ['RIGHT', 'LEFT', 'INC', 'DEC', 'SUB', 'ADD', 'NUMBER','PRINT', 'LOOP',
            'READ','DEF','PARENTESE_F','PARENTESE_A','DO','NAME']

operator = lambda type_op: (type_op)
op = lambda op: (op)
opr = lambda op, num: (op, num)

parser = ox.make_parser([
	('program : PARENTESE_A expr PARENTESE_F', lambda x,y,z: y),
    ('program : PARENTESE_A PARENTESE_F', lambda x,y: '()'),
	('expr : operator expr', lambda x,y: (x,) + y),
	('expr : operator', lambda x: (x,)),
	('operator : program', op),
    ('operator : LOOP', operator),
    ('operator : DO', operator),
    ('operator : RIGHT', operator),
    ('operator : LEFT', operator),
    ('operator : READ', operator),
    ('operator : INC', operator),
    ('operator : DEC', operator),
    ('operator : DEF', operator),
    ('operator : PRINT', operator),
    ('operator : ADD', operator),
    ('operator : SUB', operator),
    ('operator : NAME', operator),
    ('operator : NUMBER', int),
], tokens)


def dec_inc(tree,vector_aux,index,position):
    if (tree[position] == 'inc'):
        vector_aux[index] += 1
    elif (tree[position] == 'dec'):
        vector_aux[index] -= 1

    return vector_aux[index]

def run_right_left(tree, vector_aux, index,position):
        if tree[position] == 'right':
            index += 1
            if len(vector_aux) - 1 < index:
                vector_aux.append(0)
        elif tree[position] == 'left':
            index -= 1
            if index < 0:
                vector_aux.append(0)
        return index, vector_aux

def interpretador(tree,vector_aux,count):
    i = 0
    loop_active = False

    while i < len(tree):
        if isinstance(tree[i], tuple):
            vector_aux, count = interpretador(tree[i], vector_aux, count)
        elif (tree[i] == 'inc' or tree[i] == 'dec'):
            vector_aux[count] = dec_inc(tree, vector_aux, count,i)
        elif tree[i] == 'right' or tree[i] == 'left':
            count, source = run_right_left(tree, vector_aux, count,i)
        elif tree[i] == 'add':
            i += 1
            vector_aux[count] += tree[i]
        elif tree[i] == 'sub':
            i += 1
            vector_aux[count] -= tree[i]
        elif tree[i] == 'print':
            print(chr(vector_aux[count]))
        elif tree[i] == 'read':
            vector_aux[count] = input('input: ')
        elif tree[i] == 'loop':
            vector_aux, count = interpretador(tree[i], vector_aux, count)

        i += 1

    return vector_aux, count


@click.command()
@click.argument('source', type=click.File('r'))
def make_tree(source):
    vector_aux = [0]
    count = 0
    program = source.read()
    print('program: ', program)
    tokens = lexer(program)
    parser_tokens = [token for token in tokens if token.type != 'COMMENT' and token.type != 'SPACE']
    tree = parser(parser_tokens)
    interpretador(tree, vector_aux, count)
    #print(tree)

if __name__ == '__main__':
    make_tree()
