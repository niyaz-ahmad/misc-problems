# solution to problem posted on stackoverflow:
# https://stackoverflow.com/questions/75269487/pass-in-any-variable-while-guaranteeing-predefined-relationship


class Cell:
    def __add__(self, other):
        return Node(ltNode=self, rtNode=other, op='+')
    def __sub__(self, other):
        return Node(ltNode=self, rtNode=other, op='-')
    def __mul__(self, other):
        return Node(ltNode=self, rtNode=other, op='*')
    def __truediv__(self, other):
        return Node(ltNode=self, rtNode=other, op='/')

    @staticmethod
    def cleanFloat(val:int|float):
        if isinstance(val, float):
            rounded = round(val)
            if rounded == val:
                return rounded
        return val
        
            

class Leaf(Cell):
    def __init__(self, val:int|float):
        self.val = val

    @property
    def val(self):
        return self.cleanFloat(self.__val)
    @val.setter
    def val(self, val:int|float):
        self.__val = val
    
    def __call__(self, val:int|float=None):
        if val == None:
            return self.val
        else:
            self.val = val
    
    def __repr__(self):
        return f"Leaf({self.val})"
    def __str__(self):
        return f"{self.val}"
        
class Node(Cell):
    def __init__(self, ltNode:Cell, rtNode:Cell, op:str, preferredNode:Cell=None):
        self.ltNode = ltNode
        self.rtNode = rtNode
        self.op = op
        self.preferredNode = preferredNode

    @property
    def op(self):
        return self.__op
    @op.setter
    def op(self, op:str):
        self.__op = op
                
    @property
    def ltNode(self):
        return self.__ltNode
    @ltNode.setter
    def ltNode(self, ltNode:Cell):
        self.__ltNode = ltNode

    @property
    def rtNode(self):
        return self.__rtNode
    @rtNode.setter
    def rtNode(self, rtNode:Cell):
        self.__rtNode = rtNode

    @property
    def preferredNode(self):
        return self.__preferredNode
    @preferredNode.setter
    def preferredNode(self, which:Cell):
        if which == None:
            self.__preferredNode = self.rtNode
        else:
            self.__preferredNode = which

    @property
    def unPreferredNode(self):
        if self.preferredNode == self.ltNode:
            return self.rtNode
        else:
            return self.ltNode
        
    def __repr__(self):
        return f"Node( {repr(self.ltNode)}, {repr(self.rtNode)}, {repr(self.op)} )" #, {repr(self.preferredNode)} )"
    def __str__(self):
        return f"( {str(self.ltNode)} {self.op} {str(self.rtNode)} )"

    def __call__(self, val :int|float = None):
        if val == None:
            match self.op:
                case '+':
                    nodeVal =  self.ltNode() + self.rtNode()
                case '-':
                    nodeVal =  self.ltNode() - self.rtNode()
                case '*':
                    nodeVal =  self.ltNode() * self.rtNode()
                case '/':
                    nodeVal =  self.ltNode() / self.rtNode()
                case _:
                    raise
            
            return self.cleanFloat(nodeVal)
        else:
            match self.op:
                case '+':
                    self.preferredNode( val - self.unPreferredNode() )
                case '-':
                    self.preferredNode( val + self.unPreferredNode() )
                case '*':
                    self.preferredNode( val / self.unPreferredNode() )
                case '/':
                    self.preferredNode( val * self.unPreferredNode() )
                case _:
                    raise
                

if __name__ == '__main__':
    a = Leaf(2)
    b = Leaf(3)
    c = Leaf(4)
    d = a+b*c       # (b*c) is not
    e = d - Leaf(3)

    print(f"\n{e} = {e()}\n")
    
    print('## The dictionary of values has only optical purpose,')
    print(f'Printing dictionary like structure should be handled externally like this:')
    print( f"{e} => {{ 'a':{a()}, 'b':{b()}, 'c':{c()}, 'd':{d()}, 'e':{e()} }}\n")

    a(1)
    print(f"a(1) => {e} = {e()}")
    print( f"a(1) => {{ 'a':{a()}, 'b':{b()}, 'c':{c()}, 'd':{d()}, 'e':{e()} }}\n")
    b(2)
    print(f"b(2) => {e} = {e()}")
    print( f"b(2) => {{ 'a':{a()}, 'b':{b()}, 'c':{c()}, 'd':{d()}, 'e':{e()} }}\n")
    c(3)
    print(f"c(3) => {e} = {e()}")
    print( f"c(3) => {{ 'a':{a()}, 'b':{b()}, 'c':{c()}, 'd':{d()}, 'e':{e()} }}\n")

    d(627)
    print(f"d(627) => {e} = {e()}")
    print( f"d(627) => {{ 'a':{a()}, 'b':{b()}, 'c':{c()}, 'd':{d()}, 'e':{e()} }}\n")
    
    
