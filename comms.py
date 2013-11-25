import socket
from pack import *
  

class Connection:
  """ 
  Handles communication between the two bluetooth fakes.
  """
  def __init__(self,socket):
    self.sock = socket
  def __send(self, binary_data):
    self.sock.sendall(binary_data)
  def __recv(self):
    return self.sock.recv(1024)
  def send_neg(self, ID):
    self.__send(pack_neg(ID))
  def recv_neg(self):
   return unpack_neg(self.__recv())
  def send_init(self, clock, rand, link_key):
    self.__send(pack_init(clock,rand_link_key))
  def recv_init(self):
    return unpack_init(self.__recv())
  def send_data(self, clock, data):
    self.__send(pack_data(clock,data))
  def recv_data(self):
    return unpack_data(self.__recv())





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
