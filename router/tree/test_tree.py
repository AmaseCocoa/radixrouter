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

def testWork1():
    tree.insert("/uaa/:name", handle, "GET")
    tree.insert("/ubb/:name", handle, "GET")
    tree.insert("/ucc/:name", handle, "GET")
    tree.insert("/udd/:name", handle, "GET")
    tree.insert("/uee/:name", handle, "GET")
    tree.insert("/uff/:name", handle, "GET")
    tree.insert("/ugg/:name", handle, "GET")
    tree.insert("/uhh/:name", handle, "GET")
    tree.insert("/uii/:name", handle, "GET")
    tree.insert("/ujj/:name", handle, "GET")
    tree.insert("/ukk/:name", handle, "GET")
    tree.insert("/ull/:name", handle, "GET")
    tree.insert("/umm/:name", handle, "GET")
    tree.insert("/unn/:name", handle, "GET")
    tree.insert("/uoo/:name", handle, "GET")
    tree.insert("/upp/:name", handle, "GET")
    tree.insert("/uqq/:name", handle, "GET")
    tree.insert("/urr/:name", handle, "GET")
    tree.insert("/uss/:name", handle, "GET")
    tree.insert("/utt/:name", handle, "GET")
    tree.insert("/uuu/:name", handle, "GET")
    tree.insert("/uvv/:name", handle, "GET")
    tree.insert("/uww/:name", handle, "GET")
    tree.insert("/uxx/:name", handle, "GET")
    tree.insert("/uyy/:name", handle, "GET")
    tree.insert("/uzz/:name", handle, "GET")
    tree.insert("/uAA/:name", handle, "GET")
    tree.insert("/uBB/:name", handle, "GET")
    tree.insert("/uCC/:name", handle, "GET")
    tree.insert("/uDD/:name", handle, "GET")
    tree.insert("/uEE/:name", handle, "GET")
    tree.insert("/uFF/:name", handle, "GET")
    tree.insert("/uGG/:name", handle, "GET")
    tree.insert("/uHH/:name", handle, "GET")
    tree.insert("/uII/:name", handle, "GET")
    tree.insert("/uJJ/:name", handle, "GET")

    pathFound, handler, req.params = tree.get("/uss/Lime", "GET")
    if handler:
        handler(req)

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
    def f():
        for i in range(10000000):
            tree.get("/user/Lime/male/25", "GET")

    print(timeit(f, number=1))


tree = RadixTree()
req = Request("/user/Lime/male/25", "GET")

testWork1()
testPerformance()
