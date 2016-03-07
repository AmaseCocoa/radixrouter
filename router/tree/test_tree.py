# -*- coding: utf-8 -*-
"""
    Test script for Python RadixTree preformance.

    `get` run 10000000 times, about 50 seconds
"""

import sys
import os
from timeit import timeit

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))))))

from router.tree import RadixTree


class Request(object):
    def __init__(self, path, method):
        self.path = path
        self.method = method
        self.params = {}

    def __repr__(self):
        return '<Request path: {}, method: {}, params: {}>'.format(
            self.path, self.method, self.params)


def handle(req):
    print('Handled! The params are:')
    print(req.params)


def testWork():
    try:
        tree.insert("/user", handle, "GET")
        tree.insert("/user/:name", handle, "GET")
        tree.insert("/user/:name", handle, "POST")
        tree.insert("/user/:name/:sex/:age", handle, "GET")
        tree.insert("/user/lime", handle, "GET")
        tree.insert("/src/*filename", handle, "GET")
        tree.insert("/src/image.png", handle, "GET")
    except Exception as e:
        print(e)

    pathFound, handler, req.params = tree.get(req.path, req.method)
    if handler:
        handler(req)


def testPerformance():
    def run():
        tree.get(req.path, req.method)

    print(timeit(run, number=10000000))


tree = RadixTree()
req = Request("/user/Lime/male/25", "GET")

testWork()
testPerformance()
