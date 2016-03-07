Router
======

A high performance HTTP request router using Radix Tree inspired by
`httprouter <https://github.com/julienschmidt/httprouter>`_

C++ implementation VS Python implementation
-------------------------------------------

Surprisingly C++ implementation has worse performance than that of Python.

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
