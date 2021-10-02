

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
    def __init__(self, role : str, raw_argus : list) -> None:
        for a in raw_argus:
            if type(a) != StNode:
                raise TypeError
        
        self.raw_argus = raw_argus
        self.role = role
        self.argus = None
