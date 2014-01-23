import unittest 
from bitstring import *
import pack

class TestNeg(unittest.TestCase):
    def setUp(self):
        self.ID = '\xAB\xCD\xEF\xAB\xAB\xAB'
        self.packed='\x00\x00\x00\x00\xAB\xCD\xEF\xAB\xAB\xAB'
        self.type = 0
    
    def test_pack(self):
        p = pack.pack_neg(self.ID)
        self.assertEqual(p, self.packed)

    def test_unpack(self):
        p = pack.pack_neg(self.ID)
        type,id = pack.unpack_neg(self.packed)
        self.assertEqual(type, self.type)
        self.assertEqual(id, self.ID)

TestNegSuite = unittest.TestLoader().loadTestsFromTestCase(TestNeg)
unittest.TextTestRunner(verbosity=2).run(TestNegSuite)


class TestData(unittest.TestCase):
    def setUp(self):
        self.type = 2
        self.clock = 32
        self.data = 'foo'
        self.packed = '\x00\x00\x00\x02\x00\x00\x00\x20\x00\x00\x00\03foo'

    def test_pack(self):
        p = pack.pack_data(self.clock, self.data)
        self.assertEqual(p, self.packed)

    def test_unpack_data_length(self):
        l = pack.unpack_data_length(self.packed)
        self.assertEqual(len(self.data), l)

    def test_unpack_data(self):
        type,clock,length,data = pack.unpack_data(self.packed)
        self.assertEqual(type, self.type)
        self.assertEqual(clock, self.clock)
        self.assertEqual(length,len(self.data))
        self.assertEqual(data,self.data)

TestDataSuite = unittest.TestLoader().loadTestsFromTestCase(TestData)
unittest.TextTestRunner(verbosity=2).run(TestDataSuite)


