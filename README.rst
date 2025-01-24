radixrouter
======

A high performance HTTP request router using Radix Tree inspired by
`httprouter <https://github.com/julienschmidt/httprouter>`_. forked from [shiyanhui/Router](https://github.com/shiyanhui/Router)

Features
--------

- Using binary search to find child to avoid worst O(n)
- More detailed conflict information

C++ v Golang v Python
---------------------

Match path **/user/:name/:sex/:age** Ten Million times:

- Golang implementation cost about 2.7 seconds
- C++ implementation cost about 3.7 seconds
- Python implementation cost

  - CPython about 60 seconds
  - PyPy about 3.7 seconds

See `router/tree/tree.go <https://github.com/shiyanhui/Router/blob/master/router/tree/tree.go>`_,
`router/tree/test_tree.cc <https://github.com/shiyanhui/Router/blob/master/router/tree/test_tree.cc>`_ and
`router/tree/test_tree.py <https://github.com/shiyanhui/Router/blob/master/router/tree/test_tree.py>`_ for more
details.

How to use it
-------------

Unlike Golang, the Python builtin libs have poor suport for http-server side.
So you have to inherit **router.BaseRouter** for you own.

More
----

`example/ <https://github.com/shiyanhui/Router/tree/master/example>`_ contains several server-side simple examples.

License
-------

The MIT License.
