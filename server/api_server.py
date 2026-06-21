#!/usr/bin/env python3
"""
CORS Test Lab Server
Demonstrates various CORS scenarios and misconfigurations
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import time

class CORSTestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")
    
    def do_OPTIONS(self):
        print(f"\n=== PREFLIGHT REQUEST ===")
        print(f"Path: {self.path}")
        print(f"Origin: {self.headers.get('Origin', 'None')}")
        
        if self.path.startswith('/api/open'):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.send_header('Access-Control-Max-Age', '86400')
            self.end_headers()
        elif self.path.startswith('/api/restricted'):
            origin = self.headers.get('Origin', '')
            if 'localhost:8000' in origin:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', origin)
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Custom-Header')
                self.send_header('Access-Control-Allow-Credentials', 'true')
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()
    
    def do_GET(self):
        print(f"\n=== GET REQUEST === {self.path}")
        parsed = urllib.parse.urlparse(self.path)
        
        if parsed.path == '/api/open/data':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {'message': 'Open data', 'timestamp': time.time()}
            self.wfile.write(json.dumps(response).encode())
        elif parsed.path == '/api/restricted/data':
            origin = self.headers.get('Origin', '')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            if 'localhost:8000' in origin:
                self.send_header('Access-Control-Allow-Origin', origin)
                self.send_header('Access-Control-Allow-Credentials', 'true')
            self.end_headers()
            response = {'message': 'Restricted data', 'origin': origin}
            self.wfile.write(json.dumps(response).encode())
            print("⚠️  Request processed - check if CORS headers were sent!")
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        print(f"\n=== POST REQUEST === {self.path}")
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b''
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {'received': True, 'body_length': len(body)}
        self.wfile.write(json.dumps(response).encode())
        print("⚠️  POST processed - CORS doesn't prevent requests!")

def run_server(port=8001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSTestHandler)
    print(f"CORS Test API running on http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
