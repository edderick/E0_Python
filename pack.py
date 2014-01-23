# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import struct
import array
import os

def pack_neg(ID):
 type = 0
 id = ID
 data = struct.pack('>I', type) + id
 return data

def unpack_neg(data):
 type, = struct.unpack('>I', data[:4])
 id = data[4:]
 return (type,id)

def pack_init(clock, RAND, link_key):
  #clock - 26 bits, but lets send 32
  #RAND - 128 bit byte array
  #link key - 128 bit
  if len(RAND) != 16: 
    raise Exception("rand key not 128 bit") 
  if len(link_key) != 16:
    raise Exception("link key not 128 bit")

  type = 1
  data = struct.pack('>II', type, clock)
  r = array.array('B', RAND).tostring()
  l = array.array('B', link_key).tostring()
  return data + r + l

def unpack_init(data):
  d = struct.unpack('>II' + ('B' * 16) + ('B' * 16), data[:40])
  type = d[0]
  clock = d[1]
  RAND = bytearray(d[2:18])
  link_key = bytearray(d[18:34])
  return (clock, RAND, link_key)


def pack_data(clock, data):
  type = 2  
  length = len(data)
  header = struct.pack('>III', type, clock, length)
  payload = data
  d = header + payload
  return d

def unpack_data_length(data):
    type,clock,length = struct.unpack('>III', data[:12])
    return length

def unpack_data(data):
  type, clock, length = struct.unpack('>III', data[:12])  
  d = struct.unpack('>' + ('B' * length), data[12:12+length])
  d = bytearray(d)
  return (type,clock,length,d)

