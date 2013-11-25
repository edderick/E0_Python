import sys
import argparse
import comms

parser = argparse.ArgumentParser(description="Create a socket connection")
parser.add_argument('addr', type=str, default="0.0.0.0",  help="what domain name/ipaddress to connect to?")
parser.add_argument('-p', type=int, default=2000, help="port to connect to, or with -l option, port to listen on.", dest="port")
parser.add_argument('-l', dest="listen", action='store_true', help="Run as server, listen for connections.")
args = parser.parse_args()

if(args.listen):
  conn = comms.listen(args.port)
  print conn.recv(1024)
else:
  conn = comms.connect(args.addr, args.port)
  conn.send("bob")

