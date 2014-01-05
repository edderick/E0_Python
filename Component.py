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


#Examples        
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
    print i, myOutput

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
    print i, [x.bin for x in testOutput.outputs]  #display result in binary format using bin method of Bits

    
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
    print i,output
    
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
    print i,output

#Division
''' 
    Source(1)----->Divider--->Output  
'''
divider = Divider(secondTestSource)
divisionOutput = Output(divider)
for i in range(4):
    divisionOutput.step(i)
    print i,divisionOutput

