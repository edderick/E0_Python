import unittest
from bitstring import *
import comms
import thread
import socket
import time

class TestComms(unittest.TestCase):
    def start_server(self):
       self.server = comms.Connection(comms.listen(self.serversock))
    def setUp(self):
       self.port = 8005
       self.ID = 'foobar' 
       self.data = 'heres some data'
       self.clock = 11223344
       self.serversock = comms.bind(self.port)

       thread.start_new_thread(self.start_server,())
       time.sleep(2)
       self.client = comms.Connection(comms.connect(socket.getfqdn(),self.port))
       time.sleep(2)

    def tearDown(self):
        del(self.server)
        del(self.client)
        self.serversock.close()
    def test_swap_neg(self):
        self.server.send_neg(self.ID)
        self.client.send_neg(self.ID)
        self.assertEqual(self.server.recv_neg()[1], self.ID)
        self.assertEqual(self.client.recv_neg()[1], self.ID)

    def test_swap_data(self):
        self.server.send_data(self.clock, self.data)
        self.client.send_data(self.clock, self.data)
        self.assertEqual(self.server.recv_data()[-1], self.data)
        self.assertEqual(self.client.recv_data()[-1], self.data)


TestCommsSuite = unittest.TestLoader().loadTestsFromTestCase(TestComms)
unittest.TextTestRunner(verbosity=2).run(TestCommsSuite)



