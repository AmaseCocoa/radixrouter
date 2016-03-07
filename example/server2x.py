# -*- coding: utf-8 -*-
"""
    Server side example in Python2.x
"""

import sys
import os

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import socket
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from router2x import Router


class Request(BaseHTTPRequestHandler):
    def redirect(self, path):
        self.send_response(301)
        self.send_header('Location', path)
        self.end_headers()
        self.wfile.flush()

    def handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                return

            self.method = self.command
            router.handle(self)
        except socket.timeout as e:
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return


router = Router()


@router.route('/user/:name')
def user(req):
    req.send_response(200)
    req.send_header('Content-type', 'text/html')
    req.end_headers()
    req.wfile.write(req.params)
    req.wfile.flush()


def hello(req):
    req.send_response(200)
    req.send_header('Content-type', 'text/html')
    req.end_headers()
    req.wfile.write('hellow world')
    req.wfile.flush()

router.GET('/', hello)


server = HTTPServer(('127.0.0.1', 8000), Request)
server.serve_forever()
