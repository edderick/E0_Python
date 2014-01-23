import StateMachine
from bitstring import *


bd_addr = Bits('0x2c7f94560f1b')
kcp = Bits('0x2187f04aba9031d0780d4c53e0153a63')
clk = Bits('0x5f1a00') + Bits('0b10')
txt = Bits(bytes='                                                                       ')
keystream,ciphertxt =StateMachine.encipher(bd_addr, kcp, clk, txt)


f = open('sampledata4.txt')
s = f.read()

filebits = Bits(bin=s)
l = min(len(keystream), len(filebits))
print keystream[:l] == filebits[:l]

for i in range(l/8):
	print keystream[:l -l%8].hex[i], filebits[:l-l%8].hex[i]

