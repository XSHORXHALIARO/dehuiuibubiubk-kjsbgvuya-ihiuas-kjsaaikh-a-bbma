global varnames, varvalues
varnames = []
varvalues = []

def mysymplify(x):
    x = x.replace(' ', '')
    x = list(x)
    newlist = []
    newnum = ''
    abstart = 0 # absolute value / bracket expression beginning
    abstop = 0 # absolute value / bracket expression ending
    abval = ''
    abindex = [] # absolute values and brackets index
    calcnewlist = [] # list inside smallest brackets

    
    for i in range(len(x)):
        try:
            if x[i] == '.':
                newnum += x[i]
            else:
                x[i] = float(x[i])
                x[i] = str(x[i])
                newnum += x[i]
        except:
            newlist.append(float(newnum))
            newlist.append(x[i])
            newnum = ''
    while len(newlist)>1:
        i = 0
        while i < len(newlist):
            if newlist[i] == '':
                newlist.pop(i)
            elif newlist[i] == '*':
                if newlist[i+1] == '*':
                    newlist[i] = '**'
                    newlist.pop(i+1)
            elif newlist[i] == '/':
                if newlist[i+1] == '/':
                    newlist[i] = '//'
                    newlist.pop(i+1)
            elif newlist[i] == '|' or newlist[i] == '(' or newlist[i] == ')':
                abindex.append(i)
            elif newlist[i] in varnames:
                newlist[i] = varvalues[varnames.index(newlist[i])]
            
            for j in range(len(abindex)):
                if newlist[abindex[j]] == '|':
                    if newlist[abindex[j+1]] == '|':
                        abstart = abindex[j]
                        abstop = abindex[j+1]
                        abval = '||'
                        break
                    else:
                        continue
                elif newlist[abindex[j]] == '(':
                    if newlist[abindex[j+1]] == ')':
                        abstart = abindex[j]
                        abstop = abindex[j+1]
                        abval = '()'
                        break
                    else:
                        continue
            calcnewlist = newlist[abstart+1:abstop]
            calcnewlist.reverse()
            i = 0
            while i<len(calcnewlist) : # exponent loop
                if calcnewlist[i] == '**':
                    calcnewlist[i] = calcnewlist[i+1] ** calcnewlist[i-1]
                    calcnewlist.pop(i+1)
                    calcnewlist.pop(i-1)
                i+=1
            calcnewlist.reverse()
            i = 0
            while i<len(calcnewlist) : # multiplication loop
                if calcnewlist[i] == '*' or calcnewlist[i] == '/' or calcnewlist[i] == '//' or calcnewlist[i] == '%':
                    if calcnewlist[i] == '*':
                        calcnewlist[i] = calcnewlist[i+1] * calcnewlist[i-1]
                    if calcnewlist[i] == '/':
                        calcnewlist[i] = calcnewlist[i+1] / calcnewlist[i-1]
                    if calcnewlist[i] == '//':
                        calcnewlist[i] = calcnewlist[i+1] // calcnewlist[i-1]
                    if calcnewlist[i] == '%':
                        calcnewlist[i] = calcnewlist[i+1] % calcnewlist[i-1]
                    calcnewlist.pop(i+1)
                    calcnewlist.pop(i-1)
                    i+=1
            while i<len(calcnewlist) : # plus minus loop
                if calcnewlist[i] == '+' or calcnewlist[i] == '-':
                    if calcnewlist[i] == '+':
                        calcnewlist[i] = calcnewlist[i+1] + calcnewlist[i-1]
                    if calcnewlist[i] == '-':
                        calcnewlist[i] = calcnewlist[i+1] - calcnewlist[i-1]
                    calcnewlist.pop(i+1)
                    calcnewlist.pop(i-1)
                    i+=1
            if abval == '||':
                calcnewlist = abs(calcnewlist[0])
            else:
                calcnewlist = calcnewlist[0]
                calcnewlist = [calcnewlist]
            newlist = newlist[:abstart] + calcnewlist + newlist[abstop+1:]
    newlist = newlist[0]
    return newlist