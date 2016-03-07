# -*- coding: utf-8 -*-
"""
    An Router example that in Python2.x
"""

from router import BaseRouter, cleanPath, toggleTrailingSlash


class Router(BaseRouter):
    def __init__(self, redirectTrailingSlash=True, fixRequestPath=True,
                 notFoundHandler=None, methodNotAllowedHandler=None):
        self.redirectTrailingSlash = redirectTrailingSlash
        self.fixRequestPath = fixRequestPath
        self.notFoundHandler = notFoundHandler
        self.methodNotAllowedHandler = methodNotAllowedHandler

        super(Router, self).__init__()

    def handle(self, req):
        path, method = req.path, req.method.upper()
        if self.fixRequestPath:
            path = cleanPath(path)

        pathExisted, handler, req.params = self.tree.get(path, method)
        if not pathExisted:
            if self.redirectTrailingSlash:
                path = toggleTrailingSlash(path)
                pathExisted, _, _ = self.tree.get(path, method)
                if pathExisted:
                    req.redirect(path)
                    req.wfile.flush()
                    return

            if self.notFoundHandler:
                self.notFoundHandler(req)
                return

            req.send_error(404)
            req.wfile.flush()
            return

        if not handler:
            if self.methodNotAllowedHandler:
                self.methodNotAllowedHandler(req)
                return
            req.send_error(405)
            req.wfile.flush()
            return

        handler(req)
