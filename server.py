#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from linucb import ucb
from router import Router
import json
from urllib.parse import urlparse, parse_qs

class Server(BaseHTTPRequestHandler):
  def do_GET(self):
    self.__set_headers()

    data = parse_qs(urlparse(self.path).query)
    message = Router(self.command, urlparse(self.path).path, data).process()

    self.__respond(message)

  def do_POST(self):
    self.__set_headers()

    length = int(self.headers['Content-Length'])
    data = str(self.rfile.read(length), 'utf-8')

    message = Router(self.command, self.path, data).process()

    self.__respond(message)

  # Private methods

  def __set_headers(self):
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()

  def __respond(self, message, success=True):
    print(ucb.theta)

    response = {
      'success': success,
      'message': message
    }

    self.wfile.write(bytes(json.dumps(response), 'utf-8'))

print('Starting server...')

server_address = ('0.0.0.0', 8080)
httpd = HTTPServer(server_address, Server)

print('Running server...')

httpd.serve_forever()
