#!/usr/bin/python3

import http.server
import socket

class pubIpServer(http.server.HTTPServer):
  current_ip = {}

class pubIpHandler(http.server.BaseHTTPRequestHandler):

  def update_ip(self, domain, new_ip):
    if domain is None or new_ip is None:
      raise Exception('No domain or no new ip')

    if valid_ip(new_ip):
      stored_ip = self.server.current_ip.get(domain, None)

      if new_ip == stored_ip:
        raise Exception('IP was identical, skipping...')

      if 'X-Real-IP' in self.headers:
        c_ip = self.headers['X-Real-IP']
      else:
        c_ip, c_port = self.client_address
      
      if new_ip == c_ip:
        print('Updating dynamic IP for {}: {}'.format(domain, new_ip))
        self.server.current_ip[domain] = new_ip
      else:
        raise Exception('Update IP mismatch for {}: {}, {}'.format(domain, c_ip, new_ip))

  def redirect(self, domain, port):
    destination = self.server.current_ip.get(domain, None)
    if destination is None or port is None:
      raise Exception('No destination address for: {} {}'.format(domain, port))

    url = 'http://{}:{}'.format(destination, port)
    self.send_response(302)
    self.send_header('Location', url)
    self.end_headers()
    
  def do_GET(self):
    '''
      /:command/:domain/:target
      /update/vlv/127.0.0.1
      /go/vlv/8080
    '''
    msg = self.path

    if 'favico' in self.path:
      return

    action = wrassle(self.path.split('/'))

    command = action.get('command', None)
    domain = action.get('domain', None)
    target = action.get('target', None)

    if command == 'update':
      try:
        self.update_ip(domain, target)
      except Exception as e:
        print(e)

    if command == 'go':
      try:
        return self.redirect(domain, target)
      except Exception as e:
        print(e)

    if command == 'show':
      msg = self.server.current_ip.get(domain, msg) 

    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    self.wfile.write(msg.encode('utf-8'))
    return

def wrassle(array):
  result = {
    'command': None,
    'domain': None,
    'target': None
  }

  for index, value in enumerate(array):
    if value.startswith('favico'):
      continue

    if index == 1 and value:
      result['command'] = array[index]

    if index == 2 and value:
      result['domain'] = array[index]

    if index == 3 and value:
      result['target'] = array[index]

  print('Done wrasslin\': {}'.format(result))
  return result

def valid_ip(ip):
  if ip is None:
    return False

  try:
    socket.inet_aton(ip)
    return True
  except socket.error:
    print('Error on IP conversion: {}'.format(ip))
    return False

def run(server_class=pubIpServer, handler_class=pubIpHandler):
  server_address = ('', 8021)
  print('Run the server at {}'.format(server_address))
  http = server_class(server_address, handler_class)
  http.serve_forever()

if __name__ == '__main__':
  run()
