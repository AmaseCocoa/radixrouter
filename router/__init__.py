# -*- coding: utf-8 -*-

import sys

from .path import cleanPath, toggleTrailingSlash

if sys.version_info.major < 3:
    from .baserouter2x import BaseRouter
else:
    from .baserouter3x import BaseRouter


__all__ = ['BaseRouter', 'cleanPath', 'toggleTrailingSlash']
