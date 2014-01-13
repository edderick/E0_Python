# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Unit Tests
# 
# * Test Components:
#     * LSFR
#     * XOR
#     * Adder
#     * T [Bijection]
#     * Delay
#     * Output
#     * Source
#     * Divider
# * Test XORing encryption/decryption.
# 

# <codecell>

import unittest
from bitstring import *
import Component

class TestStreamXOR(unittest.TestCase):
    
    def setUp(self):
        self.plainText = Bits('0b11001100')
        self.cipherText =Bits('0b01010101')
        self.keystream = Bits('0b10011001')
        
    def test_encrypt(self):
        """Test Encryption"""
        e = self.plainText ^ self.keystream
        self.assertEqual(e, self.cipherText)
        
    def test_decrypt(self):
        """Test Decryption"""
        d = self.cipherText ^ self.keystream
        self.assertEqual(d, self.plainText)


XORSuite = unittest.TestLoader().loadTestsFromTestCase(TestStreamXOR)
unittest.TextTestRunner(verbosity=2).run(XORSuite)

# <codecell>


# <codecell>

reload(Component)

class TestAdder(unittest.TestCase):
    def setUp(self):
        self.adder = Component.Adder(3,Component.Source(Bits('0b01')), Component.Source(Bits('0b11')))
    
    def test_adder(self):
        """Test Adder(01, 11)"""
        for i in range(2):
            self.adder.step(i)
        self.assertEqual(self.adder.outputs, [Bits('0b100'), Bits('0b100')])
        #self.assertEqual(False, True)
        
TestAdderSuite = unittest.TestLoader().loadTestsFromTestCase(TestAdder)
unittest.TextTestRunner(verbosity=2).run(TestAdderSuite)

# <codecell>

reload(Component)

class TestSource(unittest.TestCase):
    def setUp(self):
        self.source = Component.Source(Bits('0b010'))
    def test_source(self):
        """ Test Source"""
        for i in range(2):
            self.source.step(i)
        self.assertEqual(self.source.outputs, [Bits('0b010'), Bits('0b010')])
        
TestSourceSuite = unittest.TestLoader().loadTestsFromTestCase(TestSource)
unittest.TextTestRunner(verbosity=2).run(TestSourceSuite)

# <codecell>

reload(Component)

class TestOutput(unittest.TestCase):
    def setUp(self):
        self.output = Component.Output(Component.Source(Bits('0b111')))
    
    def test_output(self):
        """Test Output"""
        for i in range(2):
            self.output.step(i)
        self.assertEqual(self.output.outputs, [Bits('0b111'), ('0b111')])
        
TestOutputSuite = unittest.TestLoader().loadTestsFromTestCase(TestOutput)
unittest.TextTestRunner(verbosity=2).run(TestOutputSuite)

# <codecell>

reload(Component)

class TestDelay(unittest.TestCase):
    def setUp(self):
        self.delay = Component.Delay(Bits('0b11'),Component.Source(Bits('0b110011')))
    
    def test_delay(self):
        """Test Delay"""
        for i in range(2):
            self.delay.step(i)
        self.assertEqual(self.delay.outputs, [Bits('0b11'), Bits('0b110011')])
 
TestDelaySuite = unittest.TestLoader().loadTestsFromTestCase(TestDelay)
unittest.TextTestRunner(verbosity=2).run(TestDelaySuite)

# <codecell>

reload(Component)

class TestXOR(unittest.TestCase):
    def setUp(self):
        self.xor = Component.ExclusiveOR(Component.Source(Bits('0b111')), Component.Source(Bits('0b010')))
        
    def test_xor(self):
        """Test XOR"""
        for i in range(2):
            self.xor.step(i)
        self.assertEqual(self.xor.outputs, [Bits('0b101'), Bits('0b101')])

TestXORSuite = unittest.TestLoader().loadTestsFromTestCase(TestXOR)
unittest.TextTestRunner(verbosity=2).run(TestXORSuite)
        

# <codecell>

reload(Component)

class TestDivider(unittest.TestCase):
    def setUp(self):
        self.divider = Component.Divider(Component.Source(Bits('0b100')))
        
    def test_divider(self):
        """Test Divider"""
        for i in range(2):
            self.divider.step(i)
        self.assertEqual(self.divider.outputs, [Bits('0b010'), Bits('0b010')])
                         
TestDividerSuite = unittest.TestLoader().loadTestsFromTestCase(TestDivider)
unittest.TextTestRunner(verbosity=2).run(TestDividerSuite)

# <codecell>

reload(Component)

class TestBijection(unittest.TestCase):
    def setUp(self):
        self.bijection = Component.Bijection(Component.Bijection.T2_values, Component.Source(Bits('0b11')))
    
    def test_bijection(self):
        """Test Bijection"""
        for i in range(2):
            self.bijection.step(i)
            
        self.assertEqual(self.bijection.outputs, [Bits('0b10'), Bits('0b10')])
                         
                         
TestBijectionSuite = unittest.TestLoader().loadTestsFromTestCase(TestBijection)
unittest.TextTestRunner(verbosity=2).run(TestBijectionSuite)

# <codecell>

reload(Component)

class TestLFSR(unittest.TestCase):
    def setUp(self):
        a = BitArray('0b10101')
        a.reverse()
        self.LFSR  = Component.LFSR(Component.DynamicSource(a, Bits('0b0')), Bits('0b101'), 2)
        
    def test_lfsr(self):
        """Test LSFR"""
        for i in range(6):
            self.LFSR.step(i)
        self.assertEqual(self.LFSR.outputs, [False, False, True, False ,True, False])
    
TestLFSRSuite = unittest.TestLoader().loadTestsFromTestCase(TestLFSR)
unittest.TextTestRunner(verbosity=2).run(TestLFSRSuite)
    
    

# <codecell>

reload(Component)

class TestDynamicSource(unittest.TestCase):
    def setUp(self):
        self.dsource = Component.DynamicSource(Bits('0b100'), Bits('0b0'))
    
    def test_dsource(self):
        """Test Dynamic Source"""
        for i in range(5):
            self.dsource.step(i)
        
        self.assertEqual(self.dsource.outputs, [Bits('0b0'), Bits('0b0'), Bits('0b1'), Bits('0b0'), Bits('0b0')])
        
TestDSourceSuite = unittest.TestLoader().loadTestsFromTestCase(TestDynamicSource)
unittest.TextTestRunner(verbosity=2).run(TestDSourceSuite)

# <codecell>

LFSR1_mask = Bits(uint = 139297, length = 25)        #Bits('0b0000000100010000000100001')                L1
LFSR2_mask = Bits(uint = 557185, length = 31)        #Bits('0b0000000000010001000000010000001')          L2
LFSR3_mask = Bits(uint = 536871457, length = 33)     #Bits('0b000100000000000000000001000100001')        L3
LFSR4_mask = Bits(uint = 34359740425, length = 39)   #Bits('0b000100000000000000000000000100000001001')  L4

print LFSR1_mask
print LFSR2_mask
print LFSR3_mask
print LFSR4_mask

# <codecell>


# <codecell>


# <codecell>


