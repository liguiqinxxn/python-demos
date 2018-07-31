 # -*- coding: utf-8 -*-
import math
def quadratic(a,b,c):
    m=b*b-4*a*c
    if m >=0 :
        x1=(-b+math.sqrt(m))/(2*a)
        x2=(-b-math.sqrt(m))/(2*a)
        return (x1, x2)
    else:
        print('无解')
