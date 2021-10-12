

import abc
from enum import Enum


Oper_list = ["+","-","*","/","%","<<",">>","(",")","^"]
Oper_prio = {
    ")" : 0,
    "+" : 5, "-" : 5, 
    "*" : 6, "/" : 6,
    "(" : 100,
}
Oper_func = {
    "+" : lambda a,b : a + b, 
    "-" : lambda a,b : a - b, 
    "*" : lambda a,b : a * b, 
    "/" : lambda a,b : a / b,
}


def isNum(c : str) -> bool:
    c_ord =  ord(c)
    return c == '.' or ( c_ord>= 48 and c_ord<= 57)

def isOper(c : str) -> bool:
    return c in "+-*/%<>()_^"

def isEng(c : str) -> bool:
    c_ord =  ord(c)
    return ( c_ord>= 65 and c_ord<= 90) or ( c_ord>= 97 and c_ord<= 122)


class StNode:
    class Enum_type(Enum):
        op = 'op'
        var = 'var'

    def __init__(self, op : str, raw_argus : list) -> None:
        for i,a in enumerate(raw_argus):
            #if type(a).IsSubclassOf(StNode):
            if not isinstance(a, StNode):
                raise TypeError(f"arg{i} ({a},{type(a)}) is not {StNode}.")
        self.type = None
        self.argus = raw_argus
        self.op = op

    #@abc.abstractmethod
    #def oper_func(self):
    #    return NotImplemented
    
    def __str__(self) -> str:
        line = f'[ {self.op} :'
        for a in self.argus[:-1]:
            line += f' {a} ,'
        line+=' ' + str(self.argus[-1])+' ]'
        return line

    #def compute(self):
    #    return self.oper_func()
def create_binaryOp(op, a0, a1):
    if not isinstance(a0, StNode):
        a0 = StNode_num(a0)
    if not isinstance(a1, StNode):
        a1 = StNode_num(a1)
    stn = StNode_binaryOp(op, a0, a1)
    stn.oper_func = Oper_func[op]
    return stn

class StNode_binaryOp(StNode):

    def __init__(self, op, a0, a1) -> None:
        super().__init__(op, [a0, a1])

        #self.type = self.Enum_type.op
        #self.argus = [a1, a2]
        #self.op = op

        #if op in Oper_func:
        #    self.oper_func = lambda : Oper_func[op](eval(self.argus[0]), eval(self.argus[1]))
    def compute(self):
        a0 = self.argus[0]
        a1 = self.argus[1]
        #print(a0, a1, sep=" ~ ")
        return self.oper_func( a0.compute(), a1.compute())


class StNode_unaryOp(StNode):
    def __init__(self, op : str, a1 : str) -> None:
        self.type = self.Enum_type.op
        self.argus = [a1]
        self.op = op

class StNode_num(StNode):
    def __init__(self, argu) -> None:
        self.type = self.Enum_type.var
        self.argu = argu
        if type(self.argu) == str:
            self.argu = eval(self.argu)
        #self.op = None

    def __str__(self) -> str:
        return str(self.argu)
    def compute(self):
        return self.argu
if __name__ == '__main__':
    stn = StNode('+',['1', StNode('-',[StNode_num('7'),'5'])])
    print(stn)