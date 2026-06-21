import math
import cmath
global pi, e
pi = cmath.pi
e = cmath.e
def complexdisplay(num, newimaginaryunit):
    newnum = ''
    if newimaginaryunit == 'i':
        num = list(str(num))
        for x in range(len(num)):
            if num[x] == 'j':
                num[x] = 'i'
    elif newimaginaryunit == 'j':
        for x in range(len(num)):
            if num[x] == 'i':
                num[x] = 'j'
    else:
        raise ValueError (f'{newimaginaryunit} cannot be used as a complex imaginary unit. Only "i" and "j" can be used as such.')
    for x in num:
        newnum += x
    if newimaginaryunit == 'j':
        newnum = complex(newnum)
    return newnum
def root(num, groot, rootnum = 1):
    primroot = cmath.cos(2*pi/groot) + j(cmath.sin(2*pi/groot))


    
    