#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
def run(port=8000):
    os.chdir(os.path.dirname(__file__))
    HTTPServer(('', port), Handler).serve_forever()
if __name__ == '__main__':
    run(8000)
