#!/usr/bin/python3

import http.server
import socket

class pubIpServer(http.server.HTTPServer):
  current_ip = 'n/a'


class pubIpHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()

    s_address = self.server.current_ip

    path = self.path.split('/')

    if path[1].startswith('favico'):
      return

    if path[1] == 'update':
      n_address = path[2]

      try:
        socket.inet_aton(n_address)
      except socket.error:
        print('Error on IP conversion: {}'.format(n_address))
        return

      if n_address == s_address:
        print('IP was identical, skipping...')
        return

      if 'X-Real-IP' in self.headers:
        c_address = self.headers['X-Real-IP']
      else:
        c_address, c_port = self.client_address
      
      if n_address == c_address:
        print('Updating dynamic IP: {}'.format(n_address))
        self.server.current_ip = n_address
      else:
        print('Update IP mismatch: {}, {}'.format(c_address, n_address))
        return

    msg = self.server.current_ip
    self.wfile.write(msg.encode('utf-8'))
    return


def run(server_class=pubIpServer, handler_class=pubIpHandler):
  server_address = ('', 8021)
  print('Run the server at {}'.format(server_address))
  http = server_class(server_address, handler_class)
  http.serve_forever()

if __name__ == '__main__':
  run()
