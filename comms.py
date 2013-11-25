import socket
import struct 
import array
  

class Connection:
  """ 
  Handles communication between the two bluetooth fakes.
  """
  def __init__(self,socket):
    self.socket = socket
  def __send__(self, binary_data):
    """
    Sends Network byte ordered binary data.
    """
    socket.sendall(binary_data)
  def __recv__(self):
    """
    Recieves network byte ordered binary data.
    """
    return recv(1024)
  def send_neg(ID):
    """
    Sends a negotiation packet.
    """
  def recv_neg():
    """
    Recieves negotiation packet.
    """
  def send_init():
    """
    sends init packet
    """
  def recv_init():
    """
    recieves init packet
    """
  def send_data():
   """
   sends data packet over network.
   """
  def recv_data():
   """
   recieves data packet (encrypted data).
   """





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
