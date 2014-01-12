# LFSR function

from bitstring import *

def LFSR(shift_register, tap_mask):
    while True:
        taps = tap_mask.findall([1])
        list_of_taps = list(taps)
        xor_inputs = [shift_register[tap] for tap in list_of_taps]
        def xor_operation(a,b): return a^b
        xor_result_bit = reduce(xor_operation, xor_inputs)
                
        xor_result_shifted = Bits(uint = xor_result_bit, length = shift_register.len)
        
        shift_register_update = (shift_register >> 1) | (xor_result_shifted << (shift_register.len - 1))
        shift_register = shift_register_update
        yield int(xor_result_bit), shift_register

'''
def LFSR_func(shift_register, tap_mask):
    taps = tap_mask.findall([1])
    list_of_taps = list(taps)
    xor_inputs = [shift_register[tap] for tap in list_of_taps]
    def xor_operation(a,b): return a^b
    xor_result_bit = reduce(xor_operation, xor_inputs)
                
    xor_result_shifted = Bits(uint = xor_result_bit, length = shift_register.len)
        
    shift_register_update = (shift_register >> 1) | (xor_result_shifted << (shift_register.len - 1))
    shift_register = shift_register_update
    return int(xor_result_bit), shift_register
'''
LFSR1_mask = Bits(uint = 139297, length = 25)        #Bits('0b0000000100010000000100001')                L1
LFSR2_mask = Bits(uint = 557185, length = 31)        #Bits('0b0000000000010001000000010000001')          L2
LFSR3_mask = Bits(uint = 536871457, length = 33)     #Bits('0b000100000000000000000001000100001')        L3
LFSR4_mask = Bits(uint = 34359740425, length = 39)   #Bits('0b000100000000000000000000000100000001001')  L4
count = 0
seed = Bits(uint = 25, length = 33)      #Bits('0b0000000000000000000011001')
#mask = Bits(uint = 139297, length = 25)  #Bits('0b0000000100010000000100001') L1
#seed = Bits('0b01101000010')
#seed = Bits('0b0000000000000000000011001')
mask = LFSR3_mask
# test data used to verify LFSR functionality <http://www.cs.princeton.edu/courses/archive/fall11/cos126/assignments/lfsr.html>
#seed = Bits('0b01000010110')
#mask = Bits('0b00000000101')

for xor, sr in LFSR(seed, mask):
    if (count < 25):
        print xor, sr.bin
        count += 1
    else:
        count = 0
        break

#xor, sr = LFSR_func(seed, mask)
#for i in range(20)
    


        
