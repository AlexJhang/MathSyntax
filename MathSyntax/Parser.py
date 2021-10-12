import MathSyntax.Symbols as Symb
from enum import Enum
from MathSyntax.Symbols import StNode, StNode_binaryOp, create_binaryOp

class Enum_word(Enum):
    num = "num"      #e.g., 12 -3 5.6
    oper = "oper"    #e.g., + - * ( )
    var = "VarName"  #e.g., sin x x_1
    none = None


def toTree(formular:str) -> list:
    parse_list = []
    parse_ty_list = []  
    w_stack = []

    def parseBinary():
        '''parse'''
        word = ""
        mode = Enum_word.none
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
                #print('--',c)
                if not Symb.isOper(c):
                    pushWord = True
                    if word not in Symb.Oper_list:
                        raise SyntaxError(formular, i-1, "'"+word+"' is invalid operator")
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
        #print([repr(op) for op in parse_ty_list])
    def checkWordInvalid():
        for i,c in enumerate(formular):
            if not ( Symb.isNum(c) or Symb.isEng(c) or Symb.isOper(c) or c == " "):
                raise SyntaxError(formular, i, f"'{c}' is an invalid char.")

    def postParse():
        ''''process some special symbol'''
        pass
        #[TODO] '-' : unary operator
        #[TODO] '*' : bypass '*', e.g., 5 * x = 5x
    def construct():
        '''construct tree'''
        #w_stack = []
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
            #print(w, str(ty.name))
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
            #print(w_stack, op_stack)

        while len(op_stack) > 0 and len(w_stack) >= 2:
            proc()
        #print(id(w_stack),w_stack)
        print(w_stack[0])

    # main flow
    checkWordInvalid()
    parseBinary()
    postParse()

    construct()
    #print('-',id(w_stack),w_stack)
    #print(w_stack)
    return w_stack[0]

def toNode(oper, arg0, arg1):
    return create_binaryOp(oper, arg0, arg1)

def compute(stn : list):

    def com_f(stnn):
        print(stnn)
        #if type(stnn) != list:
        if type(stnn) != StNode_binaryOp:
            print(stnn, type(stnn))
            return eval(stnn)
        else:
            return stnn.compute()
            '''
            op, a0, a1 = stnn[0], com_f(stnn[1]), com_f(stnn[2])
            if op == '+':
                return a0 + a1
            elif op == '-':
                return a0 - a1
            elif op == '*':
                return a0 * a1
            elif op == '/':
                return a0 / a1       
            '''
    
    return com_f(stn)

class SyntaxError(Exception):
    def __init__(self, line : str, pos : int, errMsg : str):
        self.line = line
        self.pos = pos
        self.errMsg = errMsg
   
    def __str__(self):
        output = "\n\t"+self.line+'\n'
        output += "\t"+" "*(self.pos)+"^\n"
        if self.errMsg != "":
            output += "Error message : " + self.errMsg + "\n"
        return output
