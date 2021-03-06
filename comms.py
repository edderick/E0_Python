import socket
from pack import *
  

class Connection:
  """ 
  Handles communication between the two bluetooth fakes.
  """
  def __init__(self,s):
    self.s = s
    self.stream = s.makefile(mode='rwb')
  def __del__(self):
      self.stream.close()
      self.s.close()
  def __send(self, binary_data):
    self.stream.write(binary_data)
    self.stream.flush()
  def __recv(self, minlength):
      return self.stream.read(minlength)
  def send_neg(self, ID):
    self.__send(pack_neg(ID))
  def recv_neg(self):
   return unpack_neg(self.__recv(10))
  def send_init(self, clock, rand, link_key):
    self.__send(pack_init(clock,rand,link_key))
  def recv_init(self):
    return unpack_init(self.__recv(40))
  def send_data(self, clock, data):
    self.__send(pack_data(clock,data))
  def recv_data(self):
      data = self.__recv(12)
      l = unpack_data_length(data)
      extra_data = self.__recv(l)
      return unpack_data(data+extra_data)


def bind(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',port))
    return s
def listen(s):
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

