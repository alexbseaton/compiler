import unittest
import context
import compiler


class TestLex(unittest.TestCase):

    def test(self):
        program = '53 + 2\n'
        expected = [compiler.Literal('53', 1, 1), compiler.Operator('+', 1, 4), compiler.Literal('2', 1, 6), compiler.Separator('\n', 1, 7)]
        actual = compiler.lex(program)
        self.assertEqual(expected, actual)


class TestParser(unittest.TestCase):

    def test(self):
        tokens = [compiler.Literal('53', 1, 1), compiler.Operator('+', 1, 4), compiler.Literal('2', 1, 6), compiler.Separator('\n', 1, 7)]
        compiler.statement(tokens, [])