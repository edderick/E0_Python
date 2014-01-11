# #Logic simulator requirements:
# 
# * Must be able to simulate simple sequential logic circuits.
# * Must be able to handle feedback (implied by above)

# <rawcell>

# #Circuit design architecture
# 
# * Circuits are made up of components.
# * Each component depends on some other components (inputs)
# 
#  e.g
#     Source(1) -------,
#                      v
#                     Adder  Here adder relies on two inputs. They provide a constant '1' and '0' respectively.
#                      ^
#     Source(0) -------'
# * The component, Output simply relays the output of its input component.
# 
#     Source(1) ----> Output ---> '1'
# 
#   The purpose of output is to be the end of the cipher stream chain of components.
#   We 'clock' by running the function 'step' of the output Component with some time t. This will automatically update all the other components to the current time step, t
# * Below is the definition of the component class and a few subclasses.
# * Below that there are a couple of examples of circuits made using this premise.
# 
# * Todo:
# 
#     - Write extra components for the other elements of the E0 cipher stream generator.
#     - Convert components written so far to use the python bitstring module instead of integers.
#     - Links components together to form the E0 cipher stream generator.
#     
# 
#     

from bitstring import *

class Component(object):
    """
    Component Class:
        Each component rerpresents some digital logic component.
        We arrange them together as neccesary.
    """
    step = -1
    def __init__(self, args):
        self.inputs = args
        self.outputs=[]
    
    def step(self,t):
        for component in self.inputs:
            while(len(component.outputs) <= t):
                component.step(t)
        self.outputs.append(self.stepfunc(t))
    
    def stepfunc(self, t):
        pass
    
    def __str__(self):
        return str(self.outputs)
        
   
class Source(Component):
    """
    Source Class:
        A component with no dependants. Always outputs a fixed value.
    """
    
    def __init__(self, value):
        self.inputs =[]
        self.outputs = []
        self.value = value
        
    def stepfunc(self, t):
        return self.value

class Output(Component):
    """
    Output Class:
        A component that depends(eventually) on all other components, but will typically depend on only one directly.
        The 'answer' is read from this component.
    """
    def __init__(self, *args):
        super(Output,self).__init__(args)
        
    def stepfunc(self, t):
        return self.inputs[0].outputs[t] # Return what its dependant  outputs
    
class Adder(Component):
    """
    Adder Class:
        Adds up its components.m
    """
    
    def __init__(self, *args):
        super(Adder,self).__init__(args)
      
    def stepfunc(self, t):
        return sum([x.outputs[t] for x in self.inputs])
    
class Delay(Component):
    """
    Delay Class:
        Output[t] = input.output[t-1]
    """
    #def __init__(self):
     #   super(Delay, self).__init__([])
      #  self.outputs.append(0)

    def __init__(self, arg):
        super(Delay, self).__init__([])
        self.outputs.append(arg)
    
    def step(self,t):
        if(len(self.outputs) == t):
            self.outputs.append(self.inputs[0].outputs[t-1])

    def stepfunc(self, t):
        return self.inputs[0].output[t-1]
    
    def addInput(self,i):
        self.inputs.append(i)

class Exclusive_OR(Component):
    """
    Exclusive_OR Class:
        Performs Exclusive-OR operation on inputs
    """
    
    def __init__(self, *args):
        super(Exclusive_OR,self).__init__(args)

    def xor(self, sequence):
        def xor_operation(a, b): return a^b
        return reduce(xor_operation, sequence)
      
    def stepfunc(self, t):
        return self.xor([x.outputs[t] for x in self.inputs])

class Divider(Component):
    """
    Divider Class:
        Performs division by 2 operation on input
    """
    
    def __init__(self, *arg):
        super(Divider, self).__init__(arg)
      
    def stepfunc(self, t):        
        return self.inputs[0].outputs[t] >> 1


class LFSR(Component):
    """
    LFSR Class:
        Models an LFSR
    """

    #Static class variables
    LFSR1_mask = Bits(uint = 139297, length = 25)        #Bits('0b0000000100010000000100001')                L1
    LFSR2_mask = Bits(uint = 557185, length = 31)        #Bits('0b0000000000010001000000010000001')          L2
    LFSR3_mask = Bits(uint = 536871457, length = 33)     #Bits('0b000100000000000000000001000100001')        L3
    LFSR4_mask = Bits(uint = 34359740425, length = 39)   #Bits('0b000100000000000000000000000100000001001')  L4
    INITIALISATION = 0
    NORMAL = 1
    OPERATION_MODE = NORMAL
    
    def __init__(self, seed, LFSR_type):
        super(LFSR,self).__init__([])
        self.result = self.LFSR_func(seed, LFSR_type)

    @classmethod
    def lfsr1(cls, seed):
        return cls(seed, LFSR.LFSR1_mask)

    @classmethod
    def lfsr2(cls, seed):
        return cls(seed, LFSR.LFSR2_mask)   

    @classmethod
    def lfsr3(cls, seed):
        return cls(seed, LFSR.LFSR3_mask)

    @classmethod
    def lfsr4(cls, seed):
        return cls(seed, LFSR.LFSR4_mask)

    def initialise(self, arg):        
        self.input_bit = arg.value        

    def LFSR_func(self, shift_register, tap_mask):
        MSB_bit = 0
        while True:
            taps = tap_mask.findall([1])
            list_of_taps = list(taps)                                   #get indices of taps
            #xor_inputs = [shift_register[tap] for tap in list_of_taps]  #use tap indices for XOR operation

            if not (self.OPERATION_MODE):
                # In initialisation operation, input bit is used to update LFSR MSB
                MSB_bit = self.input_bit.int
                
            elif (self.OPERATION_MODE):
                # In normal operation, XOR operation is used to update MSB bit of LFSR
                xor_inputs = [shift_register[tap] for tap in list_of_taps]  #use tap indices for XOR operation
                def xor_operation(a,b): return a^b
                xor_result_bit = reduce(xor_operation, xor_inputs)
                MSB_bit = xor_result_bit

            #MSB bit has to be made same length as shift register to enable OR operation
            xor_result_bit_shifted = Bits(uint = MSB_bit, length = shift_register.len)

            #Concatenate MSB and shift register (right shift LFSR)
            shift_register_update = (shift_register >> 1) | (xor_result_bit_shifted << (shift_register.len - 1))
            
            shift_register = shift_register_update
            yield int(MSB_bit)#, shift_register.bin            

    def step(self,t):
        if(len(self.outputs) == t):
            self.outputs.append(self.result.next())
      
    def stepfunc(self, t):
        return self.outputs.append(self.result.next())

#Examples

#LFSR
sr = Bits(uint = 25, length = 25)
sr_init = Bits(uint = 0, length = 25)
w = Bits('0b00')
q = Bits('0b01')

wSource = Source(w)
qSource = Source(q)

myLFSR = LFSR.lfsr1(sr_init)
#myLFSR.OPERATION_MODE = 0
#myLFSR.initialise(wSource)
LFSROutput = Output(myLFSR)

for i in range(45):
    #if (i % 2):
        #myLFSR.initialise(wSource)
    #else:
        #myLFSR.initialise(qSource)
    
    if (i < 25):
        myLFSR.OPERATION_MODE = 0
        if (sr[i]):
            m = Bits('0b01')
        else:
            m = Bits('0b00')
    else:
        myLFSR.OPERATION_MODE = 1         
    
    myLFSR.initialise(Source(m))
    LFSROutput.step(i)
    print i, LFSROutput

'''
#myLFSR = LFSR.lfsr1(sr)
for i in range(20):
    myLFSR.OPERATION_MODE = 1
    myLFSR.initialise(Source(q))
    LFSROutput.step(i)
    print i, LFSROutput
'''

'''
    Lets set up a simple circuit:
    
    Source(1)-----v
                  Adder--->Output
    Source(7)-----^
'''
m = Bits('0b0')
n = Bits('0b1')
mySource = Source(m)
mySevenSource = Source(n)
myAdder = Adder(mySource, mySevenSource)
myOutput = Output(myAdder) 
for i in range(4):
    myOutput.step(i)
    #print i, myOutput

'''
    A simple circuit for XOR:
    
    Source(0)--------v
                     |
    Source(1)-----v  |
                  Exclusive_OR--->Output
    Source(0)-----^  ^
                     |
    Source(1)--------^
'''
m = Bits('0b01')
n = Bits('0b11')
r = Bits('0b00')
testSource = Source(m)
secondTestSource = Source(n)
thirdTestSource = Source(m)
fourthTestSource = Source(n)
testXOR = Exclusive_OR(testSource, secondTestSource)# thirdTestSource, fourthTestSource)
testOutput = Output(testXOR)
for i in range(4):
    testOutput.step(i)
    #print i, [x.bin for x in testOutput.outputs]  #display result in binary format using bin method of Bits

    
'''
    Now for a more complex example.
    Lets feedback the value of an adder into a delay:

    Source(2)--------v
    Source(4)-----> Adder-----------> Output 
                     ^       |
                     |       |
                     |       |
                    delay<---'
'''

twoSource = Source(2)
fourSource = Source(4)
delay = Delay(0)
adder = Adder(twoSource, fourSource, delay)
delay.addInput(adder)
output = Output(adder)

for i in range(4):
    output.step(i)
    #print i,output
    
'''
    A more complex XOR + delay example.
    Feedback the value of an XOR into a delay:

    Source(2)--------v
    Source(4)--> Exclusive_OR-----------> Output 
                     ^       |
                     |       |
                     |       |
                    delay<---'
'''

delay = Delay(r)
#delay.addInput(r)
XOR_delayed = Exclusive_OR(testSource, secondTestSource, delay)
delay.addInput(XOR_delayed)
output = Output(XOR_delayed)

for i in range(4):
    output.step(i)
    #print i,output

#Division
''' 
    Source(1)----->Divider--->Output  
'''
divider = Divider(secondTestSource)
divisionOutput = Output(divider)
for i in range(4):
    divisionOutput.step(i)
    #print i,divisionOutput

