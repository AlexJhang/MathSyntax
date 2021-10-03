import MathSyntax.Symbols as Symb
from enum import Enum

from MathSyntax.Symbols import StNode

class Enum_word(Enum):
    num = "num"      #e.g., 12 -3 5.6
    oper = "oper"    #e.g., + - * ( )
    var = "VarName"  #e.g., sin x x_1
    none = None

def showError(line : str, pos : int, errMsg : str):
    print("[ERROR]")
    print("\t"+line)
    print("\t"+" "*(pos-1)+"^")
    print("Error message : " + errMsg)

class DivisionErr(Exception):
    def __init__(self,msg):
        self.message=msg
   
    def __str__(self):
        return self.message

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
            if Symb.isNum(c):
                mode = Enum_word.num
            elif Symb.isOper(c):
                mode =Enum_word.oper
            elif Symb.isEng(c):
                mode = Enum_word.var
            else:
                addWord = False

        elif mode == Enum_word.num:
            if not Symb.isNum(c):
                pushWord = True
                if Symb.isOper(c):
                    mode =Enum_word.oper
                elif Symb.isEng(c):
                    mode = Enum_word.var
                else:
                    mode = Enum_word.none
                    addWord = False

        elif mode == Enum_word.oper:
            if not Symb.isOper(c):
                pushWord = True
                if word not in Symb.Oper_list:
                    showError(formular, i, "'"+word+"' is invalid operator")
                    #raise()
                    return True
                if Symb.isNum(c):
                    mode = Enum_word.num
                elif Symb.isEng(c):
                    mode = Enum_word.var
                else:
                    mode = Enum_word.none
                    addWord = False
        elif mode == Enum_word.var:
            if not(Symb.isNum(c) or Symb.isEng(c) or c in "_"):
                pushWord = True
                if Symb.isOper(c):
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
            while len(op_stack) > 0 and len(w_stack) >= 2:
                if op_stack[-1] == "(":
                    if w == ")":
                        op_stack.pop()
                    break
                #print(w)
                if Symb.Oper_prio[op_stack[-1]] >= Symb.Oper_prio[w]:
                    proc()
                else:
                    break
            if w != ")":
                op_stack.append(w)

        #w_stack.append(w)
        print(w_stack, op_stack)

    while len(op_stack) > 0 and len(w_stack) >= 2:
        proc()
    print(w_stack)
    print("hello")

    return w_stack

def toNode(oper, arg1, arg2):
    return [oper, arg1, arg2]
