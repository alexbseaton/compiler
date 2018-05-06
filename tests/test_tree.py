import context
import unittest
import tree
from tree import Tree

class TestTree(unittest.TestCase):

    def setUp(self):
        self.data = Tree(5, [Tree(6, []), Tree(8, [Tree(9, [Tree(10, [])])]), Tree(3, [])])

    def test_breadth_first(self):
        expected = [0, 1, 0], True
        actual = tree.breadth_first_search(9, starting_tree=self.data)
        self.assertEquals(expected, actual)


    def test_failed_breadth_first(self):
        expected = [], False
        actual = tree.breadth_first_search(12, starting_tree=self.data)
        self.assertEquals(expected, actual)



    def test_depth_first(self):
        expected = [0, 1, 0], True
        actual = tree.depth_first_search(self.data, 9)
        self.assertEquals(expected, actual)

    def test_failed_depth_first(self):
        expected = [], False
        actual = tree.depth_first_search(self.data, 12)
        self.assertEquals(expected, actual)
