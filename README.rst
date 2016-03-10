Router
======

A high performance HTTP request router using Radix Tree inspired by
`httprouter <https://github.com/julienschmidt/httprouter>`_

Different from `httprouter <https://github.com/julienschmidt/httprouter>`_
---------------------------------------------------------------------------

- Using binary search to find child
- More detailed conflict information

C++ implementation VS Python implementation
-------------------------------------------

Match path **/user/:name/:sex/:age** ten million times:

  - C++ implementation cost about 3.7s
  - Python implementation cost about 50s

See `router/tree/test_tree.cc <https://github.com/shiyanhui/Router/blob/master/router/tree/test_tree.cc>`_ and
`router/tree/test_tree.py <https://github.com/shiyanhui/Router/blob/master/router/tree/test_tree.py>`_ for more
information.

How to use it
-------------

Unlike Golang, the Python builtin libs have poor suport for http-server side.
So you have to inherit **router.BaseRouter** for you own.

More
----

`example/ <https://github.com/shiyanhui/Router/tree/master/example>`_ contains several server-side simple examples.

Licence
-------

MIT.
