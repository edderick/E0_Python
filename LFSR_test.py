# LFSR example

def LFSR(seed, taps):
    while True:
        nxt = sum([seed[x] for x in taps]) % 2
        yield nxt
        seed = ([nxt] + seed)[:max(taps) + 1]

count = 0
for x in LFSR([1,1,0,0,1,0,0,1,0], [1,6,7,8]):
    if (count <= 20):
        print x
        count += 1
    else:
        count = 0
        break
  

def LFSR2(seed, taps):
    sr = seed
    nbits = 8
    while 1:
        xor = 1
        for t in taps:
            if (sr & (1 << (t - 1))) != 0:
                xor ^= 1
        sr = (xor << nbits - 1) + (sr >> 1)
        yield xor, sr
        if sr == seed:
            break
nbits = 9
for xor, sr in LFSR2(0b110010010, (8,7,6,1)):
    if (count <= 20):
        print xor, bin(2**nbits + sr)[3:]
        count += 1
    else:
        count = 0
        break

'''
def LFSR3(seed, mask):
    result = seed
    nbits = mask.bit_length() - 1
    while True:
        result = result << 1
        xor = result >> nbits
        if xor != 0:
            result ^= mask
        yield xor, result

for xor, pattern in LFSR3(0b110010010, 0b111000010):
        if (count <= 20):
            print xor, bin(2**nbits + pattern)[3:]
            count += 1
        else:
            count = 0
            break
'''


