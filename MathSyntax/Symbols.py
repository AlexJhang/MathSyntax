

import abc
from enum import Enum
from typing import List


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
        #for a in raw_argus:
        #    if type(a) != StNode:
        #        raise TypeError
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

class StNode_binaryOp(StNode):
    def __init__(self, op, a1, a2) -> None:
        self.type = self.Enum_type.op
        self.argus = [a1, a2]
        self.op = op

        #if op in Oper_func:
        #    self.oper_func = lambda : Oper_func[op](eval(self.argus[0]), eval(self.argus[1]))
    def compute(self):
        if self.op in Oper_func:
            a1 = self.argus[0]
            if type(a1) == StNode_binaryOp:
                a1 = a1.compute()
            if type(a1) == str:
                a1 = eval(a1)

            a2 = self.argus[1]
            if type(a2) == StNode_binaryOp:
                a2 = a2.compute()
            if type(a2) == str:
                a2 = eval(a2)
            return Oper_func[self.op]( a1, a2)
class StNode_unaryOp(StNode):
    def __init__(self, op : str, a1 : str) -> None:
        self.type = self.Enum_type.op
        self.argus = [a1]
        self.op = op

class StNode_var(StNode):
    def __init__(self, argu : str) -> None:
        self.type = self.Enum_type.var
        self.argus = [argu]
        self.op = None

    def __str__(self) -> str:
        return str(self.raw_argus[0])

if __name__ == '__main__':
    stn = StNode('+',['1', StNode('-',[StNode_var('7'),'5'])])
    print(stn)