#! /usr/bin/env python

import sys
import os
import StringIO
from math import *
import numpy
from numpy import *
from pylab import *
import matplotlib.pyplot

#N = 500 # higher modes --> produces higher tau_2  
N = 54
t0 = arange(0.01, 0.1, 0.01)
t1 = arange(0.1, 1, 0.1)
t1a = arange(1.0, 10.0, 1)
t2 = arange(10.0, 200.0, 10)
#t3 = arange(100.0, 1000.0, 100)
a = 0.0
gamma = 1.0

def gettau1(t, N, a, g):
    D1 = 0.5*a*t**(g-1)
    return (N-1)**2/pi/pi/D1

L = size(sys.argv)
if(L<3) :
    sys.stderr.write('Usage : i. Re, ii. tau')
    print 
    exit()

tau1 = False
verbose = False
carg = 1
for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-v":
            verbose = True
            carg += 1

    if word[0] == "-":
        if word == "-N":
            carg += 1
            N = int(sys.argv[carg])
            print "# number of modes: ", N
            carg += 1
            
        if word == "-tau1":
            carg += 1
            tau1 = True
            a = float(sys.argv[carg])
            carg += 1
            gamma = float(sys.argv[carg])
            print "# coefficients: ", a, gamma
            carg += 1
            

Re = float(sys.argv[carg])
carg += 1
tau = float(sys.argv[carg])
carg += 1

A = 2*Re*Re/pi/pi

for t in t0:
    gt = 0.0
    tau12 = tau 
    
    if tau1:
        tu1 = gettau1(t, N, a, gamma)
        tau12 = 1.0/(1/tu1 + 1/tau)

    for p in range(1, N):
        gt += (1 - exp(-t*p**2/tau12))/p/p

    print t, " ", A*gt

for t in t1:
    gt = 0.0
    tau12 = tau 
    
    if tau1:
        tu1 = gettau1(t, N, a, gamma)
        tau12 = 1.0/(1/tu1 + 1/tau)

    for p in range(1, N):
        gt += (1 - exp(-t*p**2/tau12))/p/p

    print t, " ", A*gt

for t in t1a:
    gt = 0.0
    tau12 = tau 
    
    if tau1:
        tu1 = gettau1(t, N, a, gamma)
        tau12 = 1.0/(1/tu1 + 1/tau)

    for p in range(1, N):
        gt += (1 - exp(-t*p**2/tau12))/p/p

    print t, " ", A*gt

for t in t2:
    gt = 0.0
    tau12 = tau 
    
    if tau1:
        tu1 = gettau1(t, N, a, gamma)
        tau12 = 1/(1/tu1 + 1/tau)
        #print tu1, tau12, 

    for p in range(1, N):
        gt += (1 - exp(-t*p**2/tau12))/p/p

    print t, " ", A*gt



