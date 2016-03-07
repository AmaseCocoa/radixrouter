# -*- coding: utf-8 -*-


def cleanPath(path):
    """Clean the path, remove `//`, './', '../'.
    """
    stack, i, n = [], 0, len(path)
    while i < n:
        string = []
        while i < n and path[i] != '/':
            string.append(path[i])
            i += 1
        i += 1

        string = ''.join(string)

        if string == '..':
            if stack:
                stack.pop()
        elif string and string != '.':
            stack.append(string)

    path = '/{}{}'.format('/'.join(stack), '/' * (path[-1] == '/'))
    return '/' if path == '//' else path


def cleanServerPath(path):
    """Clean the path, make sure catch-all parameter at end of path and after
    it no trailing slashes exist.
    """
    path, original = cleanPath(path), path

    star = path.count('*')
    if star > 1:
        raise ValueError(
            'There should be at most one catch-all parameter '
            'in "{}"'.format(original))

    if star == 1:
        if path[-1] == '/':
            path = path[:-1]

        if path[path.rfind('/') + 1] != '*':
            raise ValueError(
                'Catch-all parameter in "{}" should start '
                'with "*"'.format(original))
    return path


def toggleTrailingSlash(path):
    """Toggle trailing slash based on cleandd path
    """
    if len(path) < 2:
        return path

    return path[:-1] if path[-1] == '/' else '{}/'.format(path)
