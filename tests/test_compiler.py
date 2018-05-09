import unittest
import context
import compiler
from tree import Tree

class TestLex(unittest.TestCase):

    def test(self):
        program = '53 + 2\n'
        expected = [compiler.Number('53', 1, 1), compiler.Operator('+', 1, 4), compiler.Number('2', 1, 6), compiler.Separator('\n', 1, 7)]
        actual = compiler.lex(program)
        self.assertEqual(expected, actual)


class TestParser(unittest.TestCase):

    def test_invalid_statement(self):
        tokens = [compiler.Operator('+', 1, 1)]
        with self.assertRaises(Exception) as cm:
            compiler.statement(tokens)

    
    def test_create_ast(self):
        tokens = [compiler.Number('53', 1, 1), compiler.Operator('+', 1, 4), compiler.Number('2', 1, 6), compiler.Separator('\n', 1, 7)]
        expected = Tree(compiler.Operator('+', 1, 4), \
            [Tree(compiler.Number(53, 1, 1), []), \
            Tree(compiler.Number(2, 1, 6), [])])

        _, tree = compiler.statement(tokens)
        self.assertEqual(expected, tree)


    def test_generate_python(self):
        tree = Tree(compiler.Operator('+', 1, 4), \
            [Tree(compiler.Number(53, 1, 1), []), \
            Tree(compiler.Number(2, 1, 6), [])])
        expected = 'print(operator.add(53, 2))'
        self.assertEqual(expected, compiler.generate_python(tree))


    def test_several_statements_ast(self):
        program = '53+2\n61+54\n'
        tokens = compiler.lex(program)
        tree = compiler.program(tokens)

        left = Tree(compiler.Operator('+', 1, 3), \
            [Tree(compiler.Number(53, 1, 1), []), \
            Tree(compiler.Number(2, 1, 4), [])])

        right = Tree(compiler.Operator('+', 2, 3), \
            [Tree(compiler.Number(61, 2, 1), []), \
            Tree(compiler.Number(54, 2, 4), [])])

        expected = Tree(compiler.Program, [left, right])

        print('Expected: {}\nActual: {}\n'.format(expected, tree))

        self.assertEqual(expected, tree)


    def test_several_statements_python(self):
        program = '53+2\n61+54\n'
        tokens = compiler.lex(program)
        tree = compiler.program(tokens)
        python = compiler.generate_python(tree)
        expected = 'import operator\nprint(operator.add(53, 2))\nprint(operator.add(61, 54))'
        self.assertEqual(expected, python)