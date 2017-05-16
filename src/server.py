#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
from router import Router
import os, sys, json
from urllib.parse import urlparse, parse_qs

class Server(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.__authenticated():
      data = parse_qs(urlparse(self.path).query)
      message = Router(self.command, urlparse(self.path).path, data).process()

      self.__respond(message)

  def do_POST(self):
    if self.__authenticated():
      length = int(self.headers['Content-Length'])
      data = str(self.rfile.read(length), 'utf-8')

      message = Router(self.command, self.path, data).process()

      self.__respond(message)

  def do_DELETE(self):
    if self.__authenticated():
      message = Router(self.command, self.path, None).process()

      self.__respond(message)

  # Private methods

  def __authenticated(self):
      global key

      if key == None or (self.headers['Authorization'] == 'Bearer ' + key):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        return True
      else:
        self.send_response(403)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.__respond('Forbidden', False)

        return False

  def __respond(self, message, success=True):
    response = {
      'success': success,
      'message': message
    }

    self.wfile.write(bytes(json.dumps(response), 'utf-8'))

if __name__ == '__main__':
  if os.environ.get('LINUCB_AUTH_KEY'):
    key = os.environ['LINUCB_AUTH_KEY']
  else:
    key = None

  if key:
    print('Private mode API ...')
  else:
    print('[Warning] - Public mode API ...')

  server_address = ('0.0.0.0', 443)
  httpd = HTTPServer(server_address, Server)
  httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./cert.pem', keyfile='./cert.key', server_side=True)

  print('Running server...')

  httpd.serve_forever()
