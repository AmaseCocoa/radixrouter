# -*- coding: utf-8 -*-
"""
    Server side example in Python3.x with async mode.
"""

import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
from io import BytesIO
from http.server import BaseHTTPRequestHandler

from router3x_async import Router


class Request(BaseHTTPRequestHandler):
    def __init__(self, raw_data):
        with BytesIO(raw_data) as stream:
            self.rfile = stream
            self.raw_requestline = stream.readline()
            self.parse_request()

        self.method = self.command

    def redirect(self, path):
        # TODO
        self.writer.close()

    def send_error(self, code):
        # TODO
        self.writer.close()


async def handler(reader, writer):
    raw_data = BytesIO()
    while not reader.at_eof():
        raw_data.write(await reader.read(1024))
        reader.feed_eof()

    req = Request(raw_data.getvalue())
    raw_data.close()

    req.writer = writer
    await router.handleAsync(req)


router = Router()


@router.route('/user/:name')
async def user(req):
    r = str(req.params).encode()
    req.writer.write(r)
    req.writer.close()


async def hello(req):
    req.writer.write(b'hello world')
    req.writer.close()

router.get('/', hello)


loop = asyncio.get_event_loop()
server = loop.run_until_complete(
    asyncio.start_server(handler, '127.0.0.1', 8000, loop=loop))

try:
    loop.run_forever()
except Exception as e:
    print(e)

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
