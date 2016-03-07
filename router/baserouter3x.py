# -*- coding: utf-8 -*-
"""
    This is the base router class for Python3.x. You need to inherit this class
    for your own. Method `handle()` or `handleAsync()` need to be rewrote.
"""

from functools import partialmethod

from .tree import RadixTree
from .http import HTTP_METHODS


class RouterMeta(type):
    def __new__(cls, name, bases, attrs):
        newClass = super().__new__(cls, name, bases, attrs)

        if hasattr(newClass, 'add'):
            add = getattr(newClass, 'add')
            for m in HTTP_METHODS:
                method = partialmethod(add, methods=m)
                setattr(newClass, m, method)
                setattr(newClass, m.lower(), method)

        return newClass


class BaseRouter(metaclass=RouterMeta):
    def __init__(self):
        self.tree = RadixTree()

    def __repr__(self):
        return repr(self.tree)

    def add(self, path, handler, methods):
        self.tree.insert(path, handler, methods)

    def route(self, path, methods='GET'):
        def method(handler):
            self.add(path, handler, methods)
        return method

    def handle(self, req):
        # TODO: need rewrote
        pass

    async def handleAsync(self, req):
        # TODO: need rewrote if you write async code
        pass
