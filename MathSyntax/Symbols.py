

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
        self.raw_argus = raw_argus
        self.op = op
        self.argus = None

    @abc.abstractmethod
    def oper_func(self):
        return NotImplemented
    
    def __str__(self) -> str:
        line = f'[ {self.op} |'
        for a in self.raw_argus[:-1]:
            line += f' {a} ,'
        line+=' ' + str(self.raw_argus[-1])+' ]'
        return line

    def compute(self):
        return self.oper_func()

class StNode_binaryOp(StNode):
    def oper_func(self):
        return super().oper_func()

class StNode_var(StNode):
    def __init__(self, argu : str) -> None:
        self.type = self.Enum_type.var
        self.raw_argus = [argu]
        self.op = None
        self.argus = None

    def __str__(self) -> str:
        return str(self.raw_argus[0])

if __name__ == '__main__':
    stn = StNode('+',['1', StNode('-',[StNode_var('7'),'5'])])
    print(stn)