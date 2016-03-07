# -*- coding: utf-8 -*-
"""
    Radix Tree in Python
"""


class RadixTreeNode(object):
    def __init__(self, path=None, handler=None, methods=None):
        self.path = path
        self.methods = {}
        self.children = {}

        self.addMethods(methods, handler)

    def addMethods(self, methods, handler):
        if methods is None:
            return

        if not isinstance(methods, (list, tuple, set)):
            methods = [methods]

        for method in methods:
            if method in self.methods and self.methods[method] != handler:
                raise ValueError(
                    '{} conflicts with existed handler '
                    '{}'.format(handler, self.methods[method]))

            self.methods[method] = handler

    def __repr__(self):
        return ('<RadixTreeNode path: {}, methods: {}, children: '
                '{}>'.format(self.path, self.methods, self.children))


class RadixTree(object):
    def __init__(self):
        self.root = RadixTreeNode()

    def __repr__(self):
        return repr(self.root)

    def insert(self, key, handler, methods):
        i, n, root = 0, len(key), self.root
        getpos = lambda i: ((i + 1) % (n + 1) + n) % (n + 1)

        while i < n:
            conflict, children = [], root.children

            if ('*' in children or
                    key[i] == '*' and children or
                    key[i] != ':' and ':' in children or
                    key[i] == ':' and children and ':' not in children or
                    key[i] == ':' and ':' in children and
                    key[i + 1:getpos(key.find('/', i))] != children[':'].path):

                conflict = [key[:i] + p for p in self.traverse(root)]

            if conflict:
                raise Exception(
                    '"{}" conflicts with {}'.format(key, conflict))

            if key[i] not in root.children:
                p = getpos(key.find(':', i))
                if p == n:
                    p = getpos(key.find('*', i))
                    if p == n:
                        root.children[key[i]] = RadixTreeNode(
                            key[i:], handler, methods)
                        return

                    root.children[key[i]] = root = RadixTreeNode(key[i:p])
                    root.children['*'] = RadixTreeNode(
                        key[p + 1:], handler, methods)
                    return

                root.children[key[i]] = root = RadixTreeNode(key[i:p])

                i = getpos(key.find('/', p))
                root.children[':'] = root = RadixTreeNode(key[p + 1:i])

                if i == n:
                    root.addMethods(methods, handler)

            elif key[i] == ':':
                root = root.children[':']
                i += len(root.path) + 1

                if i == n:
                    root.addMethods(methods, handler)
            else:
                root = root.children[key[i]]
                j, m, path = 0, len(root.path), root.path

                while i < n and j < m and key[i] == path[j]:
                    i += 1
                    j += 1

                if j < m:
                    child = RadixTreeNode(path[j:])
                    child.methods, child.children = root.methods, root.children

                    root.path, root.methods = path[:j], {}
                    root.children = {path[j]: child}

                if i == n:
                    root.addMethods(methods, handler)

    def get(self, key, method):
        i, n, root, params = 0, len(key), self.root, {}
        while i < n:
            if ':' in root.children:
                root = root.children[':']
                p = ((key.find('/', i) + 1) % (n + 1) + n) % (n + 1)
                params[root.path], i = key[i:p], p
            elif '*' in root.children:
                root = root.children['*']
                params[root.path] = key[i:]
                break
            elif key[i] in root.children:
                root = root.children[key[i]]
                p = i + len(root.path)

                if key[i:p] != root.path:
                    return False, None, {}
                i = p
            else:
                return False, None, {}

        return True, root.methods.get(method, None), params

    def traverse(self, root):
        r = []
        for c in root.children:
            child = root.children[c]
            path = '{}{}'.format(c if c in [':', '*'] else '', child.path)

            if child.methods and child.children:
                r.append([path])

            r.append([path + p for p in self.traverse(child) or ['']])
        return sum(r, [])
