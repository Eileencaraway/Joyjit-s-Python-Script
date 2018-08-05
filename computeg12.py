#! /usr/bin/env python

import sys
import os
import StringIO
from math import *
import numpy
from numpy import *
from pylab import *
import matplotlib.pyplot

L = size(sys.argv)
if(L<5) :
    sys.stderr.write('Usage : i. Re, ii. tau1, iii. tau2, iv. N')
    print 
    exit()

carg = 1
Re = float(sys.argv[carg])
carg += 1
tau1 = float(sys.argv[carg])
carg += 1
tau2 = float(sys.argv[carg])
carg += 1
#tau3 = float(sys.argv[carg])
#carg += 1

N = int(sys.argv[carg])
carg += 1

A = 2*Re*Re/pi/pi
tau12 = 1/(1/tau1 + 1/tau2) 

t0 = arange(0.01, 0.1, 0.01)
t1 = arange(0.1, 1, 0.1)
t1a = arange(1.0, 10.0, 1)
t2 = arange(10.0, 200.0, 10)
#t3 = arange(100.0, 1000.0, 100)

for t in t0:
    gt = 0.0
    r = t/tau12
    for p in range(1, N):
        p2= p*p
        gt += (1 - 1/(1+p2*r))/p2
 
    print t, " ", A*gt

for t in t1:
    gt = 0.0
    r = t/tau12
    for p in range(1, N):
        p2= p*p
        gt += (1 - 1/(1+p2*r))/p2
 
    print t, " ", A*gt

for t in t1a:
    gt = 0.0
    r = t/tau12
    for p in range(1, N):
        p2= p*p
        gt += (1 - 1/(1+p2*r))/p2

    print t, " ", A*gt

for t in t2:
    gt = 0.0
    r = t/tau12
    for p in range(1, N):
        p2= p*p
        gt += (1 - 1/(1+p2*r))/p2

    print t, " ", A*gt



