import sys
from MathSyntax import toTree, compute

#formula = '(1+2) *114 + 10+2* (5+6) - sin0( -a_00) x_asd '
formula = "11 +_ 9 "
#formula = "1+3*2+4"



if __name__ == "__main__":
    #print('hello')
    #print(compute(toTree(formula)))
    toTree(formula)
    

    '''
        exec(compile(
            'for i in range(5):\r\tprint("hello")'
            , 'mulstring', 'exec'))
    '''


    sys.exit(0)
    # hi
    # Python code to demonstrate working of compile(). 
    # Creating sample sourcecode to multiply two variables 
    # x and y. 
    srcCode = 'for i in range(5):\r\tprint("hello")'
    
    # Converting above source code to an executable 
    execCode = compile(srcCode, 'mulstring', 'exec') 
    
    # Running the executable code. 
    exec(execCode)