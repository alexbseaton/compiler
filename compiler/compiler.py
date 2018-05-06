import re


def lex(path):
    with open(path, 'r') as f:
        program = f.read()

    tokens = []
    current_token = None
    for s in program:
        if current_token and current_token.isdigit() and s.isdigit():
            tokens[-1] = tokens[-1] + s
        elif s == ' ':
            continue
        else:
            tokens.append(s)

        current_token = s

    return tokens


DIGIT = 'DIGIT'
NEWLINE = 'NEWLINE'
PLUS = 'PLUS'
TYPE_TO_PATTERN = {DIGIT:r'\d+', NEWLINE:r'\n', PLUS:r'\+'}


def accept(symbol, token):
    return re.fullmatch(TYPE_TO_PATTERN[symbol], token)


def statement(tokens, tree):
    current = tokens[0]
    if accept(DIGIT, current):
        res_tokens, res_tree = operation(tokens[1:], tree)
        return newline(res_tokens, res_tree)
    else:
        raise Exception('Parse error in statement')


def operation(tokens, tree):
    current = tokens[0]
    if accept(PLUS, current):
        return digit(tokens[1:], tree)
    else:
        raise Exception('Parse error in operation')


def digit(tokens, tree):
    current = tokens[0]
    if accept(DIGIT, current):
        return tokens[1:], tree
    raise Exception('Parse error in digit')


def newline(tokens, tree):
    current = tokens[0]
    if accept(NEWLINE, current):
        return tokens[1:], tree
    raise Exception('Parse error in newline')

    