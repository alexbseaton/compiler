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

        tree = compiler.statement(tokens)
        self.assertEqual(expected, tree)


    def test_generate_python(self):
        tree = Tree(compiler.Operator('+', 1, 4), \
            [Tree(compiler.Number(53, 1, 1), []), \
            Tree(compiler.Number(2, 1, 6), [])])
        expected = 'import operator\nprint(operator.add(53, 2))'
        self.assertEqual(expected, compiler.generate_python(tree))