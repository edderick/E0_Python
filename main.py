import sys
import argparse
import comms
import os
import io
import StateMachine
import Client
import base64
from bitstring import *

parser = argparse.ArgumentParser(description="Create a socket connection")
parser.add_argument('addr', type=str, default="0.0.0.0",  help="what domain name/ipaddress to connect to?")
parser.add_argument('-p', type=int, default=2000, help="port to connect to, or with -l option, port to listen on.", dest="port")
parser.add_argument('-l', dest="listen", action='store_true', help="Run as server, listen for connections.")
args = parser.parse_args()


conn = comms.listen(args.port) if args.listen else comms.connect(args.addr, args.port)
stream = conn.makefile(mode='rwb')
conn = comms.Connection(stream)

#RAND = os.urandom(16)
ID = Bits('0b01') * 24

conn.send_neg(ID)
print 'waiting for otherID'
_,otherID = conn.recv_neg()
print 'got other ID:', otherID

masterID = max(Id, otherID)

def send_log():
   vals = {
   "CLK" : clock.uint,
   "BD_ADDR" : ID.hex,
   "is_recieving" : True,
   "keystream" : base64.b64encode(keystream.bytes),
   "ciphertext" : base64.b64encode(ciphertext.bytes),
   "plaintext" : plaintext.bytes,
   "timestamp" : '22nd janudary' }

   Client.postTo('localhost', '8000', 'log', vals, 'POST', 'master')
  

#One Direction
while(True):
 data = conn.recv_data()
 clock,plaintext = Bits(data[1], length=26), Bits(bytes=data[3])
 keystream,cipheredTxt = StateMachine.gen_keystream(masterID, kcPrime, clock,
 plaintext)
 

#Other Direction
Client.start_server()
  
  

