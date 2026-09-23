import math
global varnames, varvalues, funcnames, funclinerange, currlinenumber, errormsg, filename
filename = ''
varnames = []
varvalues = []
datatypes = []
connames = ['e', 'pi','i']
convalues = [math.e, math.pi, complex(0, 1)]
condatatypes = ['real', 'real', 'imaginary']
funcnames = [] # in built functions
customfuncnames = [] # user defined function
customfunclinerange = [] # user defined function line range
global currunitmode, unitmodes
unitmodes = ['SI', 'IMPERIAL', 'NATURAL', 'STONEY', 'PLANCK'] # overall units for quantities
currunitmode = ['SI']
currlinenumber = 0
errormsg = f'\nFILE NAME: {filename}:\nLINE NUMBER: {currlinenumber}:\n'
class Complex:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag
    def __repr__(self):
        if self.real != 0:
            if self.imag < 0:
                newimag = abs(self.imag)
                return f'{self.real} - {newimag}'
            elif self.imag == 0:
                return f'{self.real}'
            else:
                return f'{self.real} + {self.imag}'
        else:
            if self.imag < 0:
                newimag = abs(self.imag)
                return f'- {newimag}'
            elif self.imag == 0:
                return f'0'
            else:
                return f'{self.imag}' 











def listclear(x):
    x = [i for i in x if i != '']
    return x






















def findall(expression):
    expression = list(expression)
    count = 0
    newexpress = []
    while count < len(expression):
        curr = expression[count]
        if curr in '1234567890.':
            num = ''
            while count < len(expression) and expression[count] in '1234567890.':
                num += expression[count]
                count += 1
            newexpress.append(float(num))
        elif curr in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            var = ''
            while count < len(expression) and expression[count] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                var += expression[count]
                count += 1
            newexpress.append(var)
        elif curr == '/' and count + 1 < len(expression) and expression[count+1] == '/':
            newexpress.append('//')
            count += 2
        else:
            newexpress.append(curr)
            count += 1
    return listclear(newexpress)

























def mysymplify(expression): # maths simplifier ###finished
    count = 0 # all counts for while loops
    expression = expression.replace(' ', '')
    expression = findall(expression)
    
    expression = [part for part in expression if part != '']
    expression = listclear(expression) 
    for i in range(len(expression)): 
        if expression[i] in varnames:#variable replacement
            if datatypes[varnames.index(expression[i])] == 'real' or  datatypes[varnames.index(expression[i])] == 'complex' or datatypes[varnames.index(expression[i])] == 'imaginary':
                expression[i] = varvalues[varnames.index(expression[i])] # replacement
            else:
                raise TypeError(f'{errormsg}Non-number variable: {expression[i]} cannot be used in a mathematical statement.')
        elif expression[i] in connames:#constant replacement
            if condatatypes[connames.index(expression[i])] == 'real' or  condatatypes[connames.index(expression[i])] == 'complex' or condatatypes[connames.index(expression[i])] == 'imaginary':
                expression[i] = convalues[connames.index(expression[i])]
            else:
                raise TypeError(f'{errormsg}Non-number constant: "{expression[i]}" cannot be used in a mathematical statement.')
        try:
            expression[i] = float(expression[i])
        except:
            expression[i] = expression[i]
    while len(expression) > 1: # repeats till the whole expression is simplified
        bracks = [i for i in range(len(expression)) if expression[i] == '(' or expression[i] == ')'] # bracket indexes
        if len(bracks) > 0: # only checks brackcount if bracket operators exist
            while len(bracks) > 0: # repeats untill all brackets are gone
                brackcount = 0 # bracket coun - ( = +1, ) = -1, signifying a full bracket
                brackstart = bracks[0] # start of set of brackets
                brackend = 0 # end of set of brackets
                for i in bracks: # checks every bracket index
                    if expression[i] == '(': # 
                        brackcount += 1
                    elif expression[i] == ')':
                        brackcount -= 1
                    if brackcount == 0:
                        brackend = i
                        expression = expression[:brackstart] + [mysymplify(''.join(str(part) for part in expression[brackstart+1:brackend]))] + expression[brackend+1:] # recursion
                        bracks = [i for i in range(len(expression)) if expression[i] == '(' or expression[i] == ')'] # bracket indexes
                        break
        for i in range(len(expression)-1, -1, -1):
            if expression[i] == '^': # exponent
                expression[i-1] = math.pow(expression[i-1], expression[i+1])
                expression[i] = ''
                expression[i+1] = ''
        expression = listclear(expression)
        for i in range(len(expression)): # *, /, //, %
            if expression[i] == '%':
                expression[i+1] = expression[i-1]%expression[i+1]
                expression[i] = ''
                expression[i-1] = ''
            elif expression[i] == '//':
                expression[i+1] = expression[i-1]//expression[i+1]
                expression[i] = ''
                expression[i-1] = ''
            elif expression[i] == '*':
                expression[i+1] *= expression[i-1]
                expression[i] = ''
                expression[i-1] = ''
            elif expression[i] == '/':
                expression[i+1] = expression[i-1]/expression[i+1]
                expression[i] = ''
                expression[i-1] = ''
        expression = listclear(expression)
        for i in range(len(expression)): # +, -
            if expression[i] == '+':
                expression[i+1] += expression[i-1]
                expression[i] = ''
                expression[i-1] = ''
            elif expression[i] == '-':
                if i !=0:
                    expression[i+1] = expression[i-1] - expression[i+1]
                    expression[i] = ''
                    expression[i-1] = ''
                else:
                    expression[i+1] *= -1
                    expression[i] = ''
        expression = listclear(expression)
    return expression[0]
##########################################################PRINT
def show(currline): # show function examines whole line
    currline = currline[4:]
    parts = currline[1:-1]
    parts = parts.split(',')
    for j in range(len(parts)):
        while parts[j].startswith(' ') or parts[j].endswith(' '): 
            if parts[j].startswith(' '):
                parts[j] = parts[j][1:]
            if parts[j].endswith(' '):
                parts[j] = parts[j][:-1]
        if '"' in parts[j]:
            parts[j] = parts[j][1:-1]
        elif parts[j].startswith('math('):
            parts[j] = mysymplify(parts[j][5:-1])
        else:
            if parts[j] in connames:
                parts[j] = convalues[connames.index(parts[j])]
            else:  
                parts[j] = varvalues[varnames.index(parts[j])]
    print(*parts, sep="")
####################################################VARIABLES
def var(currline):
    currline = currline[4:]
    if '=' in currline and '"' not in currline:
        currline = currline.split('=')
        defin = currline[0]
        defin = defin.split(' ')
        defin = listclear(defin)
        varname = defin[1]
        datatype  = defin[0]
        if varname not in connames:
            if varname in varnames:
                datatypes[varnames.index(varname)] = datatype
                varvalues[varnames.index(varname)] = mysymplify(currline[1])
            else:
                datatypes.append(datatype)
                varnames.append(varname)
                varvalues.append(mysymplify(currline[1]))
        else:
            raise NameError(f'{errormsg}Constant "{varname}" cannot be redefined')
    elif '=' in currline:
        currline = currline.split('=', 1)
        while currline[1].startswith(' '):
            currline[1] = currline[1][1:]
        defin = currline[0]
        defin = defin.split(' ')
        defin = listclear(defin)
        datatype  = defin[0]
        varname = defin[1]
        if varname not in connames:
            if varname in varnames:
                datatypes[varnames.index(varname)] = datatype
                currline[1] = currline[1].replace('"', '')
                varvalues[varnames.index(varname)] = currline[1]
            else:
                datatypes.append(datatype)
                varnames.append(varname)
                currline[1] = currline[1].replace('"', '')
                varvalues.append(currline[1])
        else:
            raise NameError(f'Constant "{varname}" cannot be redefined')
    else:
        currline = currline.split(' ')
        currline = listclear(currline)
        datatype  = currline[0]
        varname = currline[1]
        if varname not in connames:
            if varname not in varnames:
                datatypes.append(datatype)
                varnames.append(varname)
            else:
                datatypes[varnames.index(varname)] = datatype
        else:
            raise NameError(f'{errormsg}Constant "{varname}" cannot be redefined')

def const(currline):
    currline = currline[6:]
    if '=' in currline and '"' not in currline:
        currline = currline.split('=')
        defin = currline[0]
        defin = defin.split(' ')
        defin = listclear(defin)
        varname = defin[1]
        datatype  = defin[0]
        if varname not in connames and varname not in varnames:
            condatatypes.append(datatype)
            connames.append(varname)
            convalues.append(mysymplify(currline[1]))
        else:
            if varname in varnames:
                raise NameError(f'{errormsg}Variable "{varname}" cannot be converted directly into a constant')
            else:
                raise NameError(f'{errormsg}Constant "{varname}" cannot be redefined')
    else:
        currline = currline.split('=', 1)
        while currline[1].startswith(' '):
            currline[1] = currline[1][1:]
        defin = currline[0]
        defin = defin.split(' ')
        defin = listclear(defin)
        datatype  = defin[0]
        varname = defin[1]
        if varname not in connames and varname not in varnames:
            condatatypes.append(datatype)
            connames.append(varname)
            currline[1] = currline[1].replace('"', '')
            convalues.append(currline[1])
        else:
            if varname in varnames:
                raise NameError(f'{errormsg}Variable "{varname}" cannot be converted directly into a constant')
            else:
                raise NameError(f'{errormsg}Constant "{varname}" cannot be redefined')
###########################################PARSER
def numbercode(fname):
    global currlinenumber, filename, errormsg
    filename = fname
    if filename.endswith('.ncd'):
        line = 1
        with open(f'{filename}', 'r') as file:
            lines = file.readlines()
        while line <= len(lines):
            currline = lines[line-1]
            currlinenumber = line
            currline = currline.strip()
            errormsg = f'\nFILE NAME: {filename}:\nLINE NUMBER: {currlinenumber}:\n'
            if currline.startswith('show'):
                show(currline)
            elif currline.startswith('var '):
                var(currline)
            elif currline.startswith('const '):
                const(currline)
            line+=1

    else:
        raise NameError('\n File: {filename} not found.')
    



numbercode("test.ncd")
