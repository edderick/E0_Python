# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import Component
reload(Component)

from bitstring import *

addr = Bits('0b0') * 48
kcp = Bits('0b00000000') * 16
clk = Bits('0b00') * 13

def b(bs, num):
    return bs[num*8: (num+1)*8]

initial1 = b(addr,2)+b(clk,1)+b(kcp, 12)+b(kcp,8)+b(kcp,4)+b(kcp,0)+Bits(uint = int(clk[24]), length =1)
initial1 = BitArray(initital1)
initial1.reverse()

CLU = BitArray(clk[0:4])
CLU.reverse()

CLL = BitArray(clk[4:8])
CLL.reverse()
initial2 = b(addr,3)+b(addr,0)+b(kcp,13)+b(kcp,9)+b(kcp,5)+b(kcp,1)+CLL+Bits('0b001')
initial2 = BitArray(initial2)
initial2.reverse()

initial3 = b(addr,4)+b(clk,2)+b(kcp,14)+b(kcp,10)+b(kcp,6)+b(kcp,2)+Bits(uint = int(clk[25]), length=1)
initial3 = BitArray(initial3)
initial3.reverse()

initial4 = b(addr,5)+b(addr,1)+b(addr,15)+b(kcp,15)+b(kcp,11)+b(kcp,7)+b(kcp,3)+CLU+Bits('0b111')
initial4 = BitArray(initial4)
initial4.reverse()
print "initital4", initial4.bin


mask1 = Bits(uint = 139297, length = 25)        #Bits('0b0000000100010000000100001')                L1
mask2 = Bits(uint = 557185, length = 31)        #Bits('0b0000000000010001000000010000001')          L2
mask3 = Bits(uint = 536871457, length = 33)     #Bits('0b000100000000000000000001000100001')        L3
mask4 = Bits(uint = 34359740425, length = 39)   #Bits('0b000100000000000000000000000100000001001')  L4

output1 = 23
output2 = 23
output3 = 31
output4 = 31

DSource1 = Component.DynamicSource(initial1,Bits('0b0'))
DSource2 = Component.DynamicSource(initial2,Bits('0b0'))
DSource3 = Component.DynamicSource(initial3,Bits('0b0'))
DSource4 = Component.DynamicSource(initial4,Bits('0b0'))

LFSR1 = Component.LFSR(DSource1, mask1, output1)
LFSR2 = Component.LFSR(DSource2, mask2, output2)
LFSR3 = Component.LFSR(DSource3, mask3, output3)
LFSR4 = Component.LFSR(DSource4, mask4, output4)


for i in range(240):
    LFSR1.step(i)
    LFSR2.step(i)
    LFSR3.step(i)
    LFSR4.step(i)
    print i, "X1" ,int(LFSR1.outputs[i]), "X2", int(LFSR2.outputs[i]), "X3", int(LFSR3.outputs[i]), "X4", int(LFSR4.outputs[i])
    #print i, "LSFR1", LFSR1.register,"LFSR2", LFSR2.register.bin, "LFSR3", LFSR3.register, "LFSR4", foo
    #print i, foo

# <codecell>


# <codecell>


