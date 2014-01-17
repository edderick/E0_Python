import sys
import argparse
import comms
import os
import io

parser = argparse.ArgumentParser(description="Create a socket connection")
parser.add_argument('addr', type=str, default="0.0.0.0",  help="what domain name/ipaddress to connect to?")
parser.add_argument('-p', type=int, default=2000, help="port to connect to, or with -l option, port to listen on.", dest="port")
parser.add_argument('-l', dest="listen", action='store_true', help="Run as server, listen for connections.")
args = parser.parse_args()


conn = comms.listen(args.port) if args.listen else comms.connect(args.addr, args.port)
stream = conn.makefile(mode='rwb')
conn = comms.Connection(stream)

RAND = os.urandom(16)
link_key = os.urandom(16)
ID = 5 

for clock in range(20):
 conn.send_neg(ID)
 conn.send_init(clock,RAND, link_key)
 conn.send_data(clock, 'foo')

 print conn.recv_neg()
 print conn.recv_init()
 print conn.recv_data()

conn.stream.close()


