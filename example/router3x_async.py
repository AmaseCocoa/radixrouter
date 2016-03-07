# -*- coding: utf-8 -*-
"""
    An Router example that in Python3.x with async mode
"""

from router import BaseRouter, cleanPath, toggleTrailingSlash


class Router(BaseRouter):
    def __init__(self, redirectTrailingSlash=True, fixRequestPath=True,
                 notFoundHandler=None, methodNotAllowedHandler=None):
        self.redirectTrailingSlash = redirectTrailingSlash
        self.fixRequestPath = fixRequestPath
        self.notFoundHandler = notFoundHandler
        self.methodNotAllowedHandler = methodNotAllowedHandler

        super().__init__()

    async def handleAsync(self, req):
        path, method = req.path, req.method.upper()
        if self.fixRequestPath:
            path = cleanPath(path)

        pathFound, handler, req.params = self.tree.get(path, method)
        if not pathFound:
            if self.redirectTrailingSlash:
                path = toggleTrailingSlash(path)
                pathFound, _, _ = self.tree.get(path, method)
                if pathFound:
                    req.redirect(path)
                    return

            if self.notFoundHandler:
                self.notFoundHandler(req)
                return

            req.send_error(404)
            return

        if not handler:
            if self.methodNotAllowedHandler:
                self.methodNotAllowedHandler(req)
                return
            req.send_error(405)
            return

        await handler(req)
