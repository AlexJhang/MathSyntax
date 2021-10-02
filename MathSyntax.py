from enum import Enum
from os import truncate

def isNum(c:str)->bool:
    c_ord =  ord(c)
    return c == '.' or ( c_ord>= 48 and c_ord<= 57)

def isOper(c:str)->bool:
    return c in "+-*/%<>()_^"

def isEng(c:str)->bool:
    c_ord =  ord(c)
    return ( c_ord>= 65 and c_ord<= 90) or ( c_ord>= 97 and c_ord<= 122)

Oper_list = ["+","-","*","/","%","<<",">>","(",")","^"]
Oper_prio = {
    "(" : 0,
    "+" : 5, "-" : 5, 
    "*" : 6, "/" : 6,
    ")" : 100,
}
'''
class OperNode:
    def __init__(self, symb : str) -> None:
        self.symb = symb

'''

class Enum_word(Enum):
    num = "num"
    oper = "oper"
    name = "VarName"
    none = None


class StNode:
    def __init__(self, role : str, raw_argus : list) -> None:
        self.raw_argus = raw_argus
        self.role = role
        self.argus = []


def showError(line : str, pos : int, errMsg : str):
    print("[ERROR]")
    print("\t"+line)
    print("\t"+" "*(pos-1)+"^")
    print("Error message : " + errMsg)

def toTree(formular:str) -> list:
    #parse
    word = ""
    mode = Enum_word.none
    parse_list = []
    parse_ty_list = []
    last_mode = None
    for i,c in enumerate(formular):
        pushWord = False
        addWord = True

        if mode == Enum_word.none:
            if isNum(c):
                mode = Enum_word.num
            elif isOper(c):
                mode =Enum_word.oper
            elif isEng(c):
                mode = Enum_word.name
            else:
                addWord = False

        elif mode == Enum_word.num:
            if not isNum(c):
                pushWord = True
                if isOper(c):
                    mode =Enum_word.oper
                elif isEng(c):
                    mode = Enum_word.name
                else:
                    mode = Enum_word.none
                    addWord = False

        elif mode == Enum_word.oper:
            if not isOper(c):
                pushWord = True
                if word not in Oper_list:
                    showError(formular, i, "'"+word+"' is invalid operator")
                    #raise()
                    return True
                if isNum(c):
                    mode = Enum_word.num
                elif isEng(c):
                    mode = Enum_word.name
                else:
                    mode = Enum_word.none
                    addWord = False
        elif mode == Enum_word.name:
            if not(isNum(c) or isEng(c) or c in "_"):
                pushWord = True
                if isOper(c):
                    mode = Enum_word.oper
                else:
                    mode = Enum_word.none
                    addWord = False
        

        if pushWord:
            parse_list.append(word)
            parse_ty_list.append(last_mode)
            word = ""
        if addWord:
            word+=c    
        last_mode = mode
    if mode != None:
        parse_list.append(word)
        parse_ty_list.append(last_mode)

    print(parse_list)
    print([repr(op) for op in parse_ty_list])

    #construct tree
    w_stack = []
    op_stack= []

    def proc():
        op = op_stack[-1]
        op_stack.pop()

        a1 = w_stack[-2]
        a2 = w_stack[-1]
        w_stack.pop()
        w_stack.pop()
        w_stack.append(toNode(op, a1, a2))

    for w, ty in zip(parse_list, parse_ty_list) :
        print(w, str(ty.name))
        if ty == Enum_word.num:
            w_stack.append(w)
        elif ty == Enum_word.oper:
            while len(op_stack)>0:
                #print(w)
                if Oper_prio[op_stack[-1]] > Oper_prio[w]:
                    proc()
                else:
                    break
            op_stack.append(w)

        #w_stack.append(w)
    print(w_stack, op_stack)

    for _ in range(10):
        if len(op_stack) <= 0 | len(w_stack) < 2:
            break
        proc()
    print(w_stack)

    return w_stack

def toNode(oper, arg1, arg2):
    return [oper, arg1, arg2]

def init():
    pass

init()