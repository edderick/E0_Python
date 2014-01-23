import StateMachine
from bitstring import *


bd_addr = Bits('0b0') * 48
kcp = Bits('0b0') * 128
clk = Bits('0b0') * 26
txt = Bits(bytes='                                                                       ')
keystream,ciphertxt =StateMachine.encipher(bd_addr, kcp, clk, txt)


f = open('sampledata1.txt')
s = f.read()

filebits = Bits(bin=s)
l = min(len(keystream), len(filebits))
print keystream[:l] == filebits[:l]

for i in range(l/8):
	print keystream[:l -l%8].bytes[i], filebits[:l-l%8].bytes[i]
