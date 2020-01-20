#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
from router import Router
import os, json
from urllib.parse import urlparse, parse_qs

AUTH_KEY_NAME = 'LINUCB_AUTH_KEY'

class Server(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.__authenticated():
      data = parse_qs(urlparse(self.path).query)
      message, success = Router(self.command, urlparse(self.path).path, data).process()

      self.__respond(message, success)

  def do_POST(self):
    if self.__authenticated():
      length = int(self.headers['Content-Length'])
      data = str(self.rfile.read(length), 'utf-8')

      message, success = Router(self.command, self.path, data).process()

      self.__respond(message, success)

  def do_DELETE(self):
    if self.__authenticated():
      message, success = Router(self.command, self.path, None).process()

      self.__respond(message, success)

  # Private methods

  def __authenticated(self):
    global key

    if key == None or (self.headers['Authorization'] == 'Bearer ' + key):
      return True
    else:
      self.send_response(403)
      self.end_headers()

      return False

  def __respond(self, message, success = True):
    self.send_response(200 if success else 500)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()

    if (message):
      self.wfile.write(bytes(json.dumps(message), 'utf-8'))

if __name__ == '__main__':
  key = os.environ.get(AUTH_KEY_NAME)

  if key:
    print('Private mode API ...')
  else:
    print('[Warning] - Public mode API ...')

  server_address = ('0.0.0.0', 8080)
  httpd = HTTPServer(server_address, Server)
  # httpd.socket = ssl.wrap_socket(httpd.socket, certfile='cert.pem', keyfile='cert.key', server_side=True)

  print('Running server...')

  httpd.serve_forever()
