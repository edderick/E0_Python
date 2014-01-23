import unittest
from bitstring import *
import comms
import thread
import socket
import time

class TestNeg(unittest.TestCase):
    def start_server(self):
       self.server = comms.Connection(comms.listen(self.serversock))
    def setUp(self):
       self.ID = 'foobar' 
       self.port = 8002
       self.serversock = comms.bind(self.port)
       thread.start_new_thread(self.start_server,())
       time.sleep(2)
       self.client = comms.Connection(comms.connect(socket.getfqdn(),self.port))
       time.sleep(2)

    def test_swap_neg(self):
        self.server.send_neg(self.ID)
        self.client.send_neg(self.ID)
        self.assertEqual(self.server.recv_neg()[1], self.ID)
        self.assertEqual(self.client.recv_neg()[1], self.ID)



TestNegSuite = unittest.TestLoader().loadTestsFromTestCase(TestNeg)
unittest.TextTestRunner(verbosity=2).run(TestNegSuite)
