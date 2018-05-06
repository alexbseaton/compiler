import re


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


class Literal(Token):
    pattern = r'\d+'
    def __init__(self, value, n_line, n_char):
        super(Literal, self).__init__(value, n_line, n_char)


class Separator(Token):
    pattern = r'\n'
    def __init__(self, value, n_line, n_char):
        super(Separator, self).__init__(value, n_line, n_char)


class Operator(Token):
    pattern = r'\+'
    def __init__(self, value, n_line, n_char):
        super(Operator, self).__init__(value, n_line, n_char)


types = [Literal, Separator, Operator]

def lex(program):
    res = []
    current_token = None
    n_line = 1
    n_char = 0
    for s in program:
        n_char += 1
        if current_token == Literal and re.fullmatch(Literal.pattern, s):
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
            n_line += 1

    return res


def accept(symbol, token):
    return re.fullmatch(symbol.pattern, token.value)


def statement(tokens, tree):
    current = tokens[0]
    if accept(Literal, current):
        res_tokens, res_tree = operator(tokens[1:], tree)
        return separator(res_tokens, res_tree)
    else:
        raise Exception('Parse error in statement. Expected operator but was {}'.format(current))


def operator(tokens, tree):
    current = tokens[0]
    if accept(Operator, current):
        return literal(tokens[1:], tree)
    else:
        raise Exception('Parse error in operation.')


def literal(tokens, tree):
    current = tokens[0]
    if accept(Literal, current):
        return tokens[1:], tree
    raise Exception('Parse error in digit')


def separator(tokens, tree):
    current = tokens[0]
    if accept(Separator, current):
        return tokens[1:], tree
    raise Exception('Parse error in newline')

    