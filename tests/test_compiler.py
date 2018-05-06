import unittest
import context
import compiler


class TestLex(unittest.TestCase):

    def test(self):
        expected = ['53', '+', '2', '\n']
        actual = compiler.lex('tests/program.txt')
        self.assertEqual(expected, actual)


class TestParser(unittest.TestCase):
    pass