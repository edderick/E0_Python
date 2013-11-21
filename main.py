import sys
import socket

import argparse

parser = argparse.ArgumentParser(description="Create a socket connection")
parser.add_argument('addr', type=str,  help="what domain name/ipaddress to connect to?")
parser.add_argument('-p', type=int, default=2000, help="What port to use", dest="port")
parser.add_argument('-l', dest="listen", action='store_true', help="What port to use")
args = parser.parse_args()

if(args.listen):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', args.port))
  s.listen(0)
  sess = s.accept()
  addr = sess[1]
  conn = sess[0]
  print('accepted connection from %s', addr)
  while 1:
    data = conn.recv(1024)
    print data
    if not data: break
    conn.sendall("hello, thanks for the data")
  conn.close()
else:
  conn = socket.create_connection((args.addr, args.port))
  while 1:
    data = conn.sendall("hi there")
    got = conn.recv(1024)
    if not got: break
    print got
  conn.close()

