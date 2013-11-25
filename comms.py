import socket

def listen(port):
  """
  Listen on port for incoming tcp connection.
  Accept first connection attempt and return socket handle.
  """
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', port))
  s.listen(0)
  conn, addr = s.accept()
  print('accepted connection from %s', addr)
  return conn

def connect(addr, port):
  """
  Creates tcp connection to addr (ip/hostname) on port.
  Returns handle to connected socket.
  Throws error on failure.
  """
  conn = socket.create_connection((addr, port))
  return conn
