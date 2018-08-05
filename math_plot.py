#! /usr/bin/env python

import sys
import os
import StringIO
from math import *
import numpy
from numpy import *
from pylab import *
import matplotlib.pyplot

#x = arange(0.8, 2.1, 0.01)
#x = arange(0, 1.01, 0.01)
x = arange(-5, 5, 0.1)
T = arange(0.025, 0.3, 0.01) 
B = 300.0
dg = 0.001
epsilon = 0.56 


def DeltaE(x):
    return -x**(3) + dg*x 

def funLJ(x):
    return x**(-12) - 2.0*x**(-6) 

def funLJ1(x):
    return x**(-12) - 2.0*x**(-6) + 0.1593*x**2 - 0.7295*x + 0.8528 
    
def fun(x, rcut):
    return (x + (x**2-1)**0.5) 
    
def fun2(T):
    return (T/B/epsilon)**(2.0/3.0)

def fun3(x):
    return (1 - (x)**4.0)**(2.0)

#for i in range(len(x)):
    #print x[i], funLJ(x[i]),  funLJ1(x[i])

#plot(x, funLJ(x), 'k', x, funLJ1(x), 'r', linewidth=1)

#for i in range(len(x)):
#    print x[i], fun3(x[i])
#plot(x, fun3(x), 'k', linewidth=1)

plot(x, DeltaE(x), 'k', linewidth=1)
#axis([0, 1, 0, 1.05])
#xlabel('x', x=0.9)
#ylabel('phi',rotation='vertical', y=0.82)
#xticks(fontsize='xx-large', fontstyle='italic')
#yticks(fontsize='xx-large', fontstyle='italic')

#savefig('phi.eps')
show()

def plotBinaryAndAPoint(x, y, px, py):
    plot(x, fun(x), 'k', linewidth=0.25)
    #print px, " ", py
    l = plot([px], [py], 'bo')
    axis([reform_data[0][0]-0.0001, reform_data[no_rows-1][0]+0.0001, min(fun(x))-0.001, max(fun(x))+0.001])
    setp(l, 'markersize', 4)
    #setp(l, 'markerfacecolor', 'b')

    xlabel('strain', x=0.9)
    ylabel('stress',rotation='vertical', y=0.82)
    name = 'tmp.png'
    savefig(name)

