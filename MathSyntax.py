from enum import Enum

def isNum(c:str)->bool:
    c_ord =  ord(c)
    return c == '.' or ( c_ord>= 48 and c_ord<= 57)

def isOper(c:str)->bool:
    return c in "+-*/%<>()_^"

def isEng(c:str)->bool:
    c_ord =  ord(c)
    return ( c_ord>= 65 and c_ord<= 90) or ( c_ord>= 97 and c_ord<= 122)

Oper_list = ["+","-","*","/","%","<<",">>","(",")","^"]

'''
class OperNode:
    def __init__(self, symb : str) -> None:
        self.symb = symb

'''

class WordEnum(Enum):
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

def toTree(formular:str) -> bool :
    #parse
    word = ""
    mode = WordEnum.none
    parse_list = []
    for i,c in enumerate(formular):
        pushWord = False
        addWord = True

        if mode == WordEnum.none:
            if isNum(c):
                mode = WordEnum.num
            elif isOper(c):
                mode =WordEnum.oper
            elif isEng(c):
                mode = WordEnum.name
            else:
                addWord = False

        elif mode == WordEnum.num:
            if not isNum(c):
                pushWord = True
                if isOper(c):
                    mode =WordEnum.oper
                elif isEng(c):
                    mode = WordEnum.name
                else:
                    mode = WordEnum.none
                    addWord = False

        elif mode == WordEnum.oper:
            if not isOper(c):
                pushWord = True
                if word not in Oper_list:
                    showError(formular, i, "'"+word+"' is invalid operator")
                    #raise()
                    return True
                if isNum(c):
                    mode = WordEnum.num
                elif isEng(c):
                    mode = WordEnum.name
                else:
                    mode = WordEnum.none
                    addWord = False
        elif mode == WordEnum.name:
            if not(isNum(c) or isEng(c) or c in "_"):
                pushWord = True
                if isOper(c):
                    mode = WordEnum.oper
                else:
                    mode = WordEnum.none
                    addWord = False
        

        if pushWord:
            parse_list.append(word)
            word = ""
        if addWord:
            word+=c       
    if mode != None:
        parse_list.append(word)

    print(parse_list)

    #construct tree

    w_stack = []
    for w in parse_list[:7]:
        w_stack.append(w)
        print(w_stack)


    return False


def init():
    pass

init()