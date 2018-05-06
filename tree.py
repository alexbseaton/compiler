class Tree:
    

    def __init__(self, root, subtrees):
        self._root = root
        self.subtrees = subtrees


    @property
    def root(self):
        #print('Accessing root {}'.format(self._root))
        return self._root


    def _pretty(self, n_nestings):
        res = str(self.root) + '\n'
        for subtree in self.subtrees:
            res += '\t' * n_nestings + '----> {}'.format(subtree._pretty(n_nestings + 1))
        return res


    def __str__(self):
        return self._pretty(0)


    def __repr__(self):
        return 'Tree({}, {})'.format(self.root, self.subtrees)


    def __len__(self):
        return 1 + sum(len(tree) for tree in self.subtrees)


def breadth_first_search(trees, target):
    """Returns a list of indices representing a path to target.
    For example, [] means target is the root, [0, 3] means target
    is the fourth child of the first child of root."""
    next_pass = []
    for tree, path in trees:
        if tree.root == target:
            return path, True
        for i, sub in enumerate(tree.subtrees):
            next_pass.append((sub, path + [i]))

    deeper = breadth_first_search(next_pass, target)
    if deeper[1]:
        return deeper

    return [], False


def depth_first_search(tree, target, path=[0]):
    if tree.root == target:
        return path, True

    for i, sub in enumerate(tree.subtrees):
        check = depth_first_search(sub, target, path + [i])
        if check[1]:
            return check

    return path, False


if __name__ == '__main__':
    tree = Tree(5, [Tree(6, []), Tree(8, [Tree(9, [Tree(10, [])])]), Tree(3, [])])
    print(tree)
    print('BFS:')
    print(breadth_first_search([(tree, [0])], 9))
    print('DFS')
    print(depth_first_search(tree, 9))
    print(len(tree))
