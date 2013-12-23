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
    def __init__(self):
        super(Delay, self).__init__([])
        self.outputs.append(0)
    
    def step(self,t):
        if(len(self.outputs) == t):
            self.outputs.append(self.inputs[0].outputs[t-1])
    def stepfunc(self, t):
        return self.inputs[0].output[t-1]
    
    def addInput(self,i):
        self.inputs.append(i)
'''
    Lets set up a simple circuit:
    
    Source(1)-----v
                  Adder--->Output
    Source(7)-----^
'''
mySource = Source(1)
mySevenSource = Source(7)
myAdder = Adder(mySource, mySevenSource)
myOutput = Output(myAdder) 
for i in range(4):
    myOutput.step(i)
    print i, myOutput
    
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
delay = Delay()
adder = Adder(twoSource, fourSource, delay)
delay.addInput(adder)
output = Output(adder)

for i in range(4):
    output.step(i)
    print i,output
    




