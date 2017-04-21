#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import linucb
import json
import cgi
import logging
from urllib.parse import urlparse, parse_qs

class Server(BaseHTTPRequestHandler):
  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()

  # def do_HEAD(self):
  #   self._set_headers()

  def do_GET(self):
    self._set_headers()

    data = parse_qs(urlparse(self.path).query)
    message = Router(self.command, self.path, data).process()

    self.respond(message)

  def do_POST(self):
    self._set_headers()

    length = int(self.headers['Content-Length'])
    data = str(self.rfile.read(length), 'utf-8')

    message = Router(self.command, self.path, data).process()

    self.respond(message)

  def respond(self, message):
    response = {
      'success': True,
      'message': message
    }

    self.wfile.write(bytes(json.dumps(response), 'utf-8'))

class Router(object):
  def __init__(self, command, path, args):
    self.command = command
    self.path = path
    self.args = args

  def process(self):
    postvars = cgi.parse_qs(self.args, keep_blank_values=1)

    if (self.command == 'POST'):
     if (self.path == '/teams'):
        print(postvars)
        return 'create teams'
    elif (self.command == 'GET'):
      if (self.path == '/thetas'):
        return 'get thetas'
    else:
      return 'false'

logging.warning('Starting server...')

server_address = ('127.0.0.1', 8080)
httpd = HTTPServer(server_address, Server)

print('Running server...')

httpd.serve_forever()
