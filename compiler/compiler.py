import re
from tree import Tree

class Token:


    def __init__(self, value, n_line, n_char):
        self.value = value
        self.n_line = n_line
        self.n_char = n_char


    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.value == other.value and\
        self.n_line == other.n_line and self.n_char == other.n_char


    def __repr__(self):
        return '{}[Value: [{}] n_line: [{}] n_char: [{}]]'.format(self.__class__, self.value, self.n_line, self.n_char)


class Number(Token):
    pattern = r'\d+'
    def __init__(self, value, n_line, n_char):
        super(Number, self).__init__(value, n_line, n_char)


class Separator(Token):
    pattern = r'\n'
    def __init__(self, value, n_line, n_char):
        super(Separator, self).__init__(value, n_line, n_char)


class Operator(Token):
    pattern = r'\+'
    def __init__(self, value, n_line, n_char):
        super(Operator, self).__init__(value, n_line, n_char)

class Program:
    pass


types = [Number, Separator, Operator]


def lex(program):
    res = []
    current_token = None
    n_line = 1
    n_char = 0
    for s in program:
        n_char += 1
        if current_token == Number and re.fullmatch(Number.pattern, s):
            res[-1].value = res[-1].value + s
        elif s == ' ':
            current_token = None
            continue
        else:
            candidates = [t for t in types if re.fullmatch(t.pattern, s)]
            if not candidates:
                raise Exception('Invalid symbol', s)
            elif len(candidates) > 1:
                raise Exception('Ambiguous symbol. {} matched {}'.format(s, candidates))
            res.append(candidates[0](s, n_line, n_char))
            current_token = candidates[0]

        if s == '\n':
            n_char = 0
            n_line += 1

    return res


def accept(symbol, token):
    return re.fullmatch(symbol.pattern, token.value)


def program(tokens, tree=None):
    if tree is None:
        tree = Tree(Program, [])
    if not tokens:
        return tree
    res_tokens, res_tree = statement(tokens)
    tree.subtrees.append(res_tree)
    if res_tokens:
        program(res_tokens, tree)
    return tree


def statement(tokens, tree=None):
    if tree is None:
        tree = Tree(None, [])
    current = tokens[0]
    if accept(Number, current):
        res_tokens, res_tree = separator(*operator(*number(tokens, tree)))
        return res_tokens, tree
    else:
        raise Exception('Parse error in statement. Expected Literal but was {}'.format(current))


def operator(tokens, tree):
    current = tokens[0]
    if accept(Operator, current):
        tree.root = current
        return number(tokens[1:], tree)
    else:
        raise Exception('Parse error in operator. Expected Operator but was {}'.format(current))


def number(tokens, tree):
    current = tokens[0]
    if accept(Number, current):
        tree.subtrees.append(Tree(Number(int(current.value), current.n_line, current.n_char), []))
        return tokens[1:], tree
    raise Exception('Parse error in literal. Expected Literal but was {}'.format(current))


def separator(tokens, tree):
    current = tokens[0]
    if accept(Separator, current):
        return tokens[1:], tree
    raise Exception('Parse error in separator. Expected Separator but was {}'.format(current))


def generate_python(tree):
    if tree.root == Program:
        return 'import operator\n' + '\n'.join(generate_python(subtree) for subtree in tree.subtrees)
    elif isinstance(tree.root, Operator):
        return 'print(operator.add({}, {}))'.format(generate_python(tree.subtrees[0]), generate_python(tree.subtrees[1]))
    elif isinstance(tree.root, Number):
        return str(tree.root.value)
    raise Exception('Couldn\'t generate Python for tree {}\n'.format(tree))

    