#! /usr/bin/env python

import sys
import os
import StringIO
from math import *
import numpy
from numpy import *
from pylab import *
import matplotlib.pyplot

#N = arange(10.0, 100000.0, 50)
#N = arange(10.0, 60.0, 1)

L = size(sys.argv)
if(L<6) :
    sys.stderr.write('Usage : i. Re, ii. tau1, iii. tau2, iv. tau3, v. N')
    print 
    exit()

carg = 1
Re = float(sys.argv[carg])
carg += 1
tau1 = float(sys.argv[carg])
carg += 1
tau2 = float(sys.argv[carg])
carg += 1
tau3 = float(sys.argv[carg])
carg += 1

N = int(sys.argv[carg])
carg += 1

Re2N  = Re*Re*N/54          # <Re^2(N)> proportional to N
tau1N = tau1*N*N/54/54
tau2N = tau2*N*N/54/54
#tau2N = tau2*(N**2.6)/(54**2.6)
tau3N = tau3
#if N<54:
    # tau3N = 3.85*N**1.0  # T=333
#   # tau3N = 2.9*N**0.81  # T=363
#   # tau3N = 1.4*N**0.75  # T=393
#   # tau3N = 0.72*N**0.73 # T=423

A = 2*Re2N/pi/pi
tau12 = 1/(1/tau1 + 1/tau2) 
#r = tau3/tau12
#r2 = tau3/tau2
r = tau3N/tau12
r2 = tau3N/tau2

tau12N = 1/(1/tau1N + 1/tau2N) 
#rN = tau3/tau12N
#r2N = tau3/tau2N
rN = tau3N/tau12N
r2N = tau3N/tau2N

"""
for n in N:
    gt = 0
    for p in range(1, int(n-1)):
        p2= p*p
        gt += (1 - 1/(1+p2*r))/p2

    print n, " ", A*gt/6/tau3
"""

gt = 0
gt1 = 0
gtN = 0
gt1N = 0
for p in range(1, N):
    p2= p*p
    gt += (1.0 - 1.0/(1+p2*r))/p2
    gt1 += (1.0 - 1.0/(1+p2*r2))/p2
    gtN += (1.0 - 1.0/(1+p2*rN))/p2
    gt1N += (1.0 - 1.0/(1+p2*r2N))/p2


# print N, " ", A*gt/6/tau3, " ", A*gt1/6/tau3, " ", A*gtN/6/tau3, " ", A*gt1N/6/tau3
print N, " ", A*gtN/6/tau3N, " ", A*gt1N/6/tau3N


