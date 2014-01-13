# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# #Logic simulator requirements:
# 
# * Must be able to simulate simple sequential logic circuits.
# * Must be able to handle feedback (implied by above)


# #Circuit design architecture
# 
# * Circuits are made up of components.
# * Each component depends on some other components (inputs)
# 
#  e.g
#ource(1) -------,
#                      v
#                     Adder  Here adder relies on two inputs. They provide a constant '1' and '0' respectively.
#                      ^
#ource(0) -------'
# * The component, Output simply relays the output of its input component.
# 
#ource(1) ----> Output ---> '1'
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
ource Class:
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
    def __init__(self,*args):
        super(Output,self).__init__(args)
        
    def stepfunc(self, t):
        return self.inputs[0].outputs[t] # Return what its dependant  outputs
    
class Adder(Component):
    """
    Adder Class:
        Adds up its components.m
    """
    
    def __init__(self, outputLength, *inputs):
        self.outputLength = outputLength
        super(Adder,self).__init__(inputs)
      
    def stepfunc(self, t):
        return Bits(uint = reduce( lambda x,y: x.outputs[t].uint + y.outputs[t].uint , self.inputs) % 2**self.outputLength, length = self.outputLength)
    
class Delay(Component):
    """
    Delay Class:
        Output[t] = input.output[t-1]
    """
    #def __init__(self):
     #   super(Delay, self).__init__([])
      #  self.outputs.append(0)

    def __init__(self, initialValue, arg):
        super(Delay, self).__init__([arg])
        self.initialValue = initialValue
    
    def astep(self,t):
        if(len(self.outputs) == t):
            self.outputs.append(self.stepfunc(t))

    def stepfunc(self, t):
        print t
        return  self.initialValue if t ==0 else self.inputs[0].outputs[t-1]
    
    def addInput(self,i):
        self.inputs.append(i)

class ExclusiveOR(Component):
    """
    Exclusive_OR Class:
        Performs Exclusive-OR operation on inputs
    """
    
    def __init__(self, *args):
        super(ExclusiveOR,self).__init__(args)

    def xor(self, sequence):
        return reduce(lambda a,b: a^b, sequence)
      
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

class Bijection(Component):
    """
    Bijection Class:
        A bijection on some input
    """

    #Static class variables
    T1_values = [Bits('0b00'), Bits('0b01'), Bits('0b10'), Bits('0b11')]
    T2_values = [Bits('0b00'), Bits('0b11'), Bits('0b01'), Bits('0b10')]
    
    def __init__(self,b, arg):
        self.bijection = b
        super(Bijection, self).__init__([arg])
      
    def stepfunc(self, t):   
        return self.bijection[self.inputs[0].outputs[t].uint]
       

class DynamicSource(Component):
    """
    A dynamic Source class, returns a bit from dynamic until it runs out, then returns the same bit, static repeatedly
    """
    def __init__(self, dynamic, static):
        self.dynamic = dynamic
        self.static = static
        super(DynamicSource, self).__init__([])
        
    def stepfunc(self,t):
        return Bits(uint= int(self.dynamic[t]), length= 1) if t < len(self.dynamic) else self.static
        

class LFSR(Component):
    """LFSR Class """
    
    def __init__(self, dsource, mask, output_bit):
        self.mask = mask
        self.register = BitArray(uint = 0, length = len(mask))
        self.outputBit = output_bit
        super(LFSR, self).__init__([dsource])
        
    def stepfunc(self, t):
        inputBit = self.inputs[0].outputs[t]
        taps = list(self.mask.findall([1]))
        xorInputs = [self.register[tap] for tap in taps]
        
        retval = self.register[self.outputBit]
        if(t >= len(self.mask)):
           xorInputs.append(bool(inputBit))
           input = Bits(uint = int(reduce(lambda x,y: x^y, xorInputs)), length = 1)
        else:
            input = inputBit
        self.register >>=1
        self.register = self.register | (input * len(self.register)) << (len(self.register) -1)
        return retval
    
class LFSRA(Component):
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
    OPERATION_MODE = NORMAL                             # default operation mode is normal operation
    MASK_TYPE = 0
    
    def __init__(self, seed, LFSR_type):
        super(LFSR,self).__init__([])
        self.result = self.LFSR_func(seed, LFSR_type)
        self.counter = 0

    @classmethod
    def lfsr1(cls, seed):
        cls.MASK_TYPE = 1
        return cls(seed, LFSR.LFSR1_mask)

    @classmethod
    def lfsr2(cls, seed):
        cls.MASK_TYPE = 2
        return cls(seed, LFSR.LFSR2_mask)   

    @classmethod
    def lfsr3(cls, seed):
        cls.MASK_TYPE = 3
        return cls(seed, LFSR.LFSR3_mask)

    @classmethod
    def lfsr4(cls, seed):
        cls.MASK_TYPE = 4
        return cls(seed, LFSR.LFSR4_mask)

    def initialise(self, arg):        
        self.input_bit = arg.value        

    def LFSR_func(self, shift_register, tap_mask):
        MSB_bit = 0
        #counter = 0
        while True:
            taps = tap_mask.findall([1])
            list_of_taps = list(taps)                                   #get indices of taps
            xor_inputs = [shift_register[tap] for tap in list_of_taps]  #use tap indices for XOR operation
            def xor_operation(a,b): return a^b

            if not (self.OPERATION_MODE):
                # In initialisation operation, input bit is used to update LFSR MSB
                # Switch is closed when first input bit reaches right most position of LFSR
                # When switch is closed, input bit is XOR'd with xor operation result to give
                # new MSB_bit (not sure why I'm commenting this; seems obvious from code already!)
                if (self.counter < tap_mask.len):
                    MSB_bit = self.input_bit.int
                elif (self.counter >= tap_mask.len):
                    xor_result_bit = reduce(xor_operation, xor_inputs)
                    MSB_bit = self.input_bit.int ^ xor_result_bit
                
            elif (self.OPERATION_MODE):
                # In normal operation, XOR operation is used to update MSB bit of LFSR
                #xor_inputs = [shift_register[tap] for tap in list_of_taps]  #use tap indices for XOR operation
                #def xor_operation(a,b): return a^b
                xor_result_bit = reduce(xor_operation, xor_inputs)
                MSB_bit = xor_result_bit

            #MSB bit has to be made same length as shift register to enable OR operation
            xor_result_bit_shifted = Bits(uint = MSB_bit, length = shift_register.len)

            #Concatenate MSB and shift register (right shift LFSR)
            shift_register_update = (shift_register >> 1) | (xor_result_bit_shifted << (shift_register.len - 1))
            
            shift_register = shift_register_update
            
            #Select output bit depending on LFSR type
            if (self.MASK_TYPE == 1) | (self.MASK_TYPE == 2):
                X = shift_register[23]
            elif (self.MASK_TYPE == 3) | (self.MASK_TYPE == 4):
                X = shift_register[31]

            if (X):
                X_bit = Bits('0b01')
            elif not (X):
                X_bit = Bits('0b00')
            yield int(MSB_bit)#, X_bit.int , shift_register.bin
            self.counter += 1

    def step(self,t):
        if(len(self.outputs) == t):
            self.outputs.append(self.result.next())
      
    def stepfunc(self, t):
        return self.outputs.append(self.result.next())


# <codecell>


# <codecell>


