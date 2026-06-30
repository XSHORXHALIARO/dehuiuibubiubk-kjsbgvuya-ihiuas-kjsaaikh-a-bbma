import math
global varnames, varvalues, funcnames, funclinerange
varnames = []
varvalues = []
datatypes = []
connames = ['e', 'pi','i']
convalues = [math.e, math.pi, complex(0, 1)]
condatatypes = ['real', 'real', 'imaginary']
funcnames = [] # in built functions
customfuncnames = [] # user defined function
customfunclinerange = [] # user defined function line range
unitmodes = ['SI', 'IMPERIAL', 'NATURAL', 'STONEY', 'PLANCK'] # overall units for quantities
















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
        elif expression[i] in connames:#constant replacement
            if condatatypes[connames.index(expression[i])] == 'real' or  condatatypes[connames.index(expression[i])] == 'complex' or condatatypes[connames.index(expression[i])] == 'imaginary':
                expression[i] = convalues[connames.index(expression[i])]
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
            try:
                parts[j] = mysymplify(parts[j][5:-1])
            except:
                parts[j] = parts[j]
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
            raise ValueError
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
            raise ValueError
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
            raise ValueError

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
            datatypes.append(datatype)
            varnames.append(varname)
            varvalues.append(mysymplify(currline[1]))
        else:
            raise ValueError
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
            datatypes.append(datatype)
            varnames.append(varname)
            currline[1] = currline[1].replace('"', '')
            varvalues.append(currline[1])
        else:
            raise ValueError
###########################################PARSER
def numbercode(filename):
    if filename.endswith('.ncd'):
        line = 1
        with open(f'{filename}', 'r') as file:
            lines = file.readlines()
        while line <= len(lines):
            currline = lines[line-1]
            currline = currline.strip()
            if currline.startswith('show'):
                show(currline)
            elif currline.startswith('var '):
                var(currline)
            elif currline.startswith('const '):
                const(currline)
            line+=1

    else:
        raise NameError
    



numbercode("test.ncd")
