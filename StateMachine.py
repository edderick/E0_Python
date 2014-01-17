# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import Component
reload(Component)

from bitstring import *

reqBytes = 16
addr = Bits('0x2c7f94560f1b')
kcp = Bits('0x2187f04aba9031d0780d4c53e0153a63')
clk = Bits('0x5f1a00') + Bits('0b10')

def b(bs, num):
    return bs[num*8: (num+1)*8]

print "clock", len(clk), clk
print "addr", len(addr),addr
print "kcp", len(kcp),kcp
print "kcp[0]", b(kcp,0).bin
print "clk[24]", clk[24]

initial1 = b(addr,2)+b(clk,1)+b(kcp, 12)+b(kcp,8)+b(kcp,4)+b(kcp,0)+Bits(uint = int(clk[23]), length =1)
initial1 = BitArray(initial1)
initial1.reverse()

print "initital1",initial1

CLU = BitArray(clk[0:4])
#CLU.reverse()

CLL = BitArray(clk[4:8])
CLL.reverse()

initial2 = b(addr,3)+b(addr,0)+b(kcp,13)+b(kcp,9)+b(kcp,5)+b(kcp,1)+CLL+Bits('0b001')
initial2 = BitArray(initial2)
initial2.reverse()

initial3 = b(addr,4)+b(clk,2)+b(kcp,14)+b(kcp,10)+b(kcp,6)+b(kcp,2)+Bits(uint = int(clk[24]), length=1)
initial3 = BitArray(initial3)
initial3.reverse()

initial4 = b(addr,5)+b(addr,1)+b(addr,15)+b(kcp,15)+b(kcp,11)+b(kcp,7)+b(kcp,3)+CLU+Bits('0b111')
initial4 = BitArray(initial4)
initial4.reverse()



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

LFSRAdder = Component.Adder(3, LFSR1, LFSR2, LFSR3, LFSR4)

blendAdder = Component.Adder(3, LFSRAdder)

divider = Component.Divider(2, blendAdder)

blendXOR = Component.ExclusiveOR(divider)

topDelay =Component.Delay(Bits('0b00'),blendXOR)

T1 = Component.Bijection(Component.Bijection.T1_values, topDelay)

bottomDelay = Component.Delay(Bits('0b00'),topDelay)

T2 = Component.Bijection(Component.Bijection.T2_values, bottomDelay)

blendSlice = Component.Slice(1,2, topDelay)

bigXOR = Component.ExclusiveOR(LFSR1, LFSR2, LFSR3, LFSR4, blendSlice)

blendAdder.addInput(topDelay)
blendXOR.addInput(T1)
blendXOR.addInput(T2)


output = Component.Output(bigXOR)

registers = []

for i in range(240):
    ou1 = BitArray(LFSR1.register)
    ou1.reverse()
    ou2 = BitArray(LFSR2.register)
    ou2.reverse()
    ou3 = BitArray(LFSR3.register)
    ou3.reverse()
    ou4 = BitArray(LFSR4.register)
    ou4.reverse()

    registers.append((Bits(uint = ou1.uint, length=28).hex, Bits(uint = ou2.uint, length=32).hex, Bits(uint = ou3.uint, length =36).hex, Bits(uint = ou4.uint, length=40).hex))


    if(i <=40):
        topDelay.outputs[-1] = Bits('0b00')
        bottomDelay.outputs[-1] = Bits('0b00')

    output.step(i)


Z = output.outputs[112:240] #Last 128 bits generated

temp = Z[0]
for x in Z[1:]:
    temp+=x

Z = temp
#print "Z", Z
update1 = b(Z,0)+b(Z,4)+b(Z,8)+Z[12*8:(12*8)+1]

l2 = BitArray(Z[(12*8)+1:13*8])
#l2.reverse()
update2 = b(Z,1)+b(Z,5)+b(Z,9)+l2

update3 = b(Z,2)+b(Z,6)+b(Z,10)+b(Z,13)+Z[15*8:(15*8)+1]

l4 = BitArray(Z[(15*8)+1:16*8])
#l4.reverse()
update4 = b(Z,3)+b(Z,7)+b(Z,11)+b(Z,14)+l4

#print "update1", update1
#print "update2", update2
#print "update3", update3
#print "update4", update4

LFSR1.register = update1
LFSR2.register = update2
LFSR3.register = update3
LFSR4.register = update4

#blendXOR.outputs.append(blendXOR.outputs[-1])

print "len", len(topDelay.outputs), len(bottomDelay.outputs), len(blendXOR.outputs)
blendXOR.step(239)

topDelay.outputs.append(topDelay.outputs[-1])
bottomDelay.outputs.append(bottomDelay.outputs[-1])
#bottomDelay.outputs.append(bottomDelay.outputs[-1])

#while(len(blendXOR.outputs) <= 240):
 #   blendXOR.outputs.append(Bits('0b00'))

for i in range(240,500):
    ou1 = BitArray(LFSR1.register)
    ou1.reverse()
    ou2 = BitArray(LFSR2.register)
    ou2.reverse()
    ou3 = BitArray(LFSR3.register)
    ou3.reverse()
    ou4 = BitArray(LFSR4.register)
    ou4.reverse()

    registers.append((Bits(uint = ou1.uint, length=28).hex, Bits(uint = ou2.uint, length=32).hex, Bits(uint = ou3.uint, length =36).hex, Bits(uint = ou4.uint, length=40).hex))

    output.step(i)



keystream = BitArray()
for bit in output.outputs[240:240+reqBytes*8]:
    keystream +=bit
#print [x.bin for x in output.outputs[240:]]

#for i in range(reqBytes):
#    print b(keystream,i).uint
#print keystream

    
for i in range(340):
    print i, registers[i][0], registers[i][1], registers[i][2], registers[i][3], "    ",LFSR1.outputs[i].bin, LFSR2.outputs[i].bin, LFSR3.outputs[i].bin, LFSR4.outputs[i].bin, "   ", output.outputs[i].bin,  "    ",blendXOR.outputs[i].bin, \
            topDelay.outputs[i].bin, bottomDelay.outputs[i].bin


keystream = BitArray()
for i in output.outputs[240:240+(reqBytes*8)]:
    keystream +=i


for i in range(reqBytes):
    print b(keystream,i).uint
print keystream
    #print i, "                                 ", LFSR1.outputs[i].bin, LFSR2.outputs[i].bin, LFSR3.outputs[i].bin, LFSR4.outputs[i].bin,"   ",output.outputs[i].bin, blendXOR.outputs[i].bin, "   ",topDelay.outputs[i].bin, bottomDelay.outputs[i].bin #,"blendslice[t]", blendSlice.outputs[i].bin
    #print i, "Z", output.outputs[i].bin, "LSFRs", LFSR1.outputs[i].bin, LFSR2.outputs[i].bin, LFSR3.outputs[i].bin, LFSR4.outputs[i].bin, "C[t+1]", blendXOR.outputs[i].bin, "C[t]", topDelay.outputs[i].bin 
    #print i, foo
    #print i, output.outputs[i].bin

# <codecell>


# <codecell>

