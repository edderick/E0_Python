import Component
from bitstring import *

def encipher(masterAddr, kcPrime, clock, txt):

  print 'clock: ', clock.uint
  reqBits = len(txt)

  addr = masterAddr
  kcp = kcPrime
  clk = clock

  def b(bs, num):
      return bs[num*8: (num+1)*8]

  #First 4 bits
  CLU = BitArray(clk[0:4])
  #Last 4 bits reversed
  CLL = BitArray(clk[4:8])
  CLL.reverse()

  #LFSR1 initials
  initial1 = b(addr,2)+b(clk,1)+b(kcp, 12)+b(kcp,8)+b(kcp,4)+b(kcp,0)+Bits(uint = int(clk[23]), length =1)
  initial1 = BitArray(initial1)
  initial1.reverse()

  #LFSR2 initials
  initial2 = b(addr,3)+b(addr,0)+b(kcp,13)+b(kcp,9)+b(kcp,5)+b(kcp,1)+CLL+Bits('0b001')
  initial2 = BitArray(initial2)
  initial2.reverse()

  #LFSR3 initials
  initial3 = b(addr,4)+b(clk,2)+b(kcp,14)+b(kcp,10)+b(kcp,6)+b(kcp,2)+Bits(uint = int(clk[24]), length=1)
  initial3 = BitArray(initial3)
  initial3.reverse()

  #LFSR4 initials
  initial4 = b(addr,5)+b(addr,1)+b(addr,15)+b(kcp,15)+b(kcp,11)+b(kcp,7)+b(kcp,3)+CLU+Bits('0b111')
  initial4 = BitArray(initial4)
  initial4.reverse()


  #LFSR feedback masks
  mask1 = Bits(uint = 139297, length = 25)        #Bits('0b0000000100010000000100001')                L1
  mask2 = Bits(uint = 557185, length = 31)        #Bits('0b0000000000010001000000010000001')          L2
  mask3 = Bits(uint = 536871457, length = 33)     #Bits('0b000100000000000000000001000100001')        L3
  mask4 = Bits(uint = 34359740425, length = 39)   #Bits('0b000100000000000000000000000100000001001')  L4


  #LFSR output bit positions
  output1 = 23
  output2 = 23
  output3 = 31
  output4 = 31

  #Dynamicources
  DSource1 = Component.DynamicSource(initial1,Bits('0b0'))
  DSource2 = Component.DynamicSource(initial2,Bits('0b0'))
  DSource3 = Component.DynamicSource(initial3,Bits('0b0'))
  DSource4 = Component.DynamicSource(initial4,Bits('0b0'))

  #LFSRs
  LFSR1 = Component.LFSR(DSource1, mask1, output1)
  LFSR2 = Component.LFSR(DSource2, mask2, output2)
  LFSR3 = Component.LFSR(DSource3, mask3, output3)
  LFSR4 = Component.LFSR(DSource4, mask4, output4)


  #Componentetup
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


  #Do initial 240 iterations
  for i in range(240):
      if(i <=40):
          topDelay.outputs[-1] = Bits('0b00')
          bottomDelay.outputs[-1] = Bits('0b00')
      output.step(i)


  Z = output.outputs[112:240] #Last 128 bits generated

  #Create Z
  temp = Z[0]
  for x in Z[1:]:
      temp+=x
  Z = temp

  #Update LFSR registers
  update1 = b(Z,0)+b(Z,4)+b(Z,8)+Z[12*8:(12*8)+1]

  l2 = BitArray(Z[(12*8)+1:13*8])
  update2 = b(Z,1)+b(Z,5)+b(Z,9)+l2

  update3 = b(Z,2)+b(Z,6)+b(Z,10)+b(Z,13)+Z[15*8:(15*8)+1]

  l4 = BitArray(Z[(15*8)+1:16*8])
  update4 = b(Z,3)+b(Z,7)+b(Z,11)+b(Z,14)+l4

  LFSR1.register = update1
  LFSR2.register = update2
  LFSR3.register = update3
  LFSR4.register = update4


  #Hold Ct and Ct-1
  blendXOR.step(239)
  topDelay.outputs.append(topDelay.outputs[-1])
  bottomDelay.outputs.append(bottomDelay.outputs[-1])


  #Generate keystream
  for i in range(240, 240+reqBits):
      output.step(i)


  #Turn into bit array
  keystream = reduce(lambda x,y: x+y, output.outputs[240:])

  cipheredTxt = keystream ^ txt
  return keystream,cipheredTxt


