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
            if abs(rounded-val)<0.011:
                return rounded
            else:
                return round(val, 2)
        return val


class Leaf(Cell):
    def __init__(self, val:int|float):
        self.val = val

    @property
    def val(self):
        return self.cleanFloat(self.__val)
    @val.setter
    def val(self, val:int|float):
        self.__val = self.cleanFloat(val)
    
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
    def __init__(self, ltNode:Cell, rtNode:Cell, op:str, 
                 prefPath:str='right'):
        self.ltNode = ltNode
        self.rtNode = rtNode
        self.op = op
        self.prefPath = prefPath

    @property
    def preferredNode(self):
        match self.prefPath:
            case 'left' : return self.ltNode
            case 'right': return self.rtNode

    @property
    def unPreferredNode(self):
        match self.prefPath:
            case 'left' : return self.rtNode
            case 'right': return self.ltNode

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
                case '*':
                    self.preferredNode( val / self.unPreferredNode() )
                case '-':
                    match self.prefPath:
                        case 'left'  : 
                            self.preferredNode( val + self.unPreferredNode() )
                        case 'right' : 
                            self.preferredNode( self.unPreferredNode() - val )
                case '/':
                    match self.prefPath:
                        case 'left ' : 
                            self.preferredNode( val * self.unPreferredNode() )
                        case 'right' : 
                            self.preferredNode( self.unPreferredNode() / val )
                case _:
                    raise
        
    def __repr__(self):
        return f"Node( {repr(self.ltNode)}, {repr(self.rtNode)}, {repr(self.op)} )" #, {repr(self.preferredNode)} )"
    def __str__(self):
        return f"( {str(self.ltNode)} {self.op} {str(self.rtNode)} )"
                

if __name__ == '__main__':
    # create new Leaf nodes having values
    a = Leaf(2)
    b = Leaf(3)
    c = Leaf(4)
    
    # define relationships
    d = a + b*c       # (b*c) becomes anonymous
    e = d - Leaf(3)   # Leaf(3) is anonymous

    print('\nget values of known nodes (also note the anonymous nodes):')
    print(f"{e} => {{ 'a':{a()}, 'b':{b()}, 'c':{c()}, 'd':{d()}, 'e':{e()} }}\n")
    

    print('update values:')
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
    print(f"d(627) => {{ 'a':{a()}, 'b':{b()}, 'c':{c()}, 'd':{d()}, 'e':{e()} }}\n")
    
    e(10)
    print(f"e(10) => {e} = {e()}")
    print(f"e(10) => {{ 'a':{a()}, 'b':{b()}, 'c':{c()}, 'd':{d()}, 'e':{e()} }}\n")

    # change ordering preference
    e.prefPath = 'left'
    e(100)
    print(f"e(100) => {e} = {e()}")
    print(f"e(100) => {{ 'a':{a()}, 'b':{b()}, 'c':{c()}, 'd':{d()}, 'e':{e()} }}\n")
