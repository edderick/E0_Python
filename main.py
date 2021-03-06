import sys
import argparse
import comms
import os
import io
import Client
import base64
from bitstring import *
import StateMachine
import socket
import thread
import g


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Create a socket connection")
	parser.add_argument('addr', type=str, default="0.0.0.0",  help="what domain name/ipaddress to connect to?")
	parser.add_argument('-p', type=int, default=2000, help="port to connect to, or with -l option, port to listen on.", dest="port")
	parser.add_argument('-l', dest="listen", action='store_true', help="Run as server, listen for connections.")
	parser.add_argument('-k', type=int, default=8888, help="Port to talk to web server with", dest='httpPort')
	args = parser.parse_args()


	g.clock = Bits('0b0') * 26
	g.kcPrime = Bits('0b0') * 128
	#Server or Client?
	if(args.listen):
	    serversock = comms.bind(args.port)
	    g.conn = comms.Connection(comms.listen(serversock))
	else:
	    g.conn = comms.Connection(comms.connect(socket.getfqdn(), args.port))

	g.httpPort = args.httpPort
	print 'httpPort: ', g.httpPort

	g.ID = Bits(bytes = os.urandom(6))
	g.conn.send_neg(g.ID.bytes)
	print 'waiting for otherID'
	g.otherID = Bits(bytes=g.conn.recv_neg()[1])
	print 'got other ID:', g.otherID


	def master(ours, theirs):
	    o = ours.bytes
	    t = theirs.bytes
	    for i in range(len(o)):
		if(o[i] > t[i]):
		    return ours
		elif(t[i] > o[i]):
		    return theirs



	g.masterID = master(g.ID, g.otherID)
	print 'Master BD_ADDR is: ', g.masterID



	def do_sockets():
		while(True):
		 data = g.conn.recv_data()
		 print "Recieved some Data"
		 temp = BitArray(uint=data[1], length=26)

		 g.clock,plaintext = temp, Bits(bytes=data[3])

		 rev = BitArray(g.clock)
		 rev.reverse()
		 print "clock: ", g.clock
		 keystream,cipheredTxt =StateMachine.encipher(g.masterID, g.kcPrime, rev,
		 plaintext)
		 g.send_log('true', g.ID == g.masterID, keystream, plaintext, cipheredTxt)


	thread.start_new_thread(do_sockets, ())
	print 'started sockets thread'
	Client.MyWebServer().start()



	#thread.start_new_thread(Client.start_server(), ())









