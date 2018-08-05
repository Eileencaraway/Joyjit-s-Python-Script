#!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *
from random import *
from pylab import *
from matplotlib import pyplot, mpl

L = sys.argv
first = 0
values = 0
sq_values = 0
sum_column = 0

L = size(sys.argv)
if(L<3) :
    sys.stderr.write('Usage : i. number of atoms, ii. time ')
    print 
    exit()

carg    = 1
verbose = False
D       = 1
npos    = -1
for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-v":
            verbose = True
            carg += 1

        if word == "-D":    # diffusion coefficient 
            carg += 1
            D = float(sys.argv[carg])
            carg += 1

        if word == "-npos": # nb. of atoms moving along the positive direction
            carg += 1
            npos = int(sys.argv[carg])
            carg += 1

N = int(sys.argv[carg])
carg += 1
t = float(sys.argv[carg])
carg += 1

if npos==-1:
    npos=N/2

MSD = 2*D*t
dx   = zeros(N, 'f')

####################################################################################
### when dx_i = +/- sqrt(MSD):
for i in range(N):
    if i < npos:
        dx[i] = sqrt(MSD)
    else:
        dx[i] = -sqrt(MSD)


### when dx is a Gaussian Distribution with mean zero and variance 2Dt:
dx = [gauss(0.0, sqrt(2*D*t)) for i in range(N)]

val=0
for i in range(N):
    val += dx[i]**2

MSD = val/N

### Log normal distribution ... if you take the natural logarithm of this distribution you will get a normal distribution with mean mu and standard deviation sigma .. mu can have any value and sigma must be greater than zero
"""
dx2 = [lognormvariate(2.34, 1.15) for i in range(N/2)]
for i in range(N/2):
    dx[i]  = -sqrt(dx2[i]) 
for i in range(N/2, N):
    dx[i]  = sqrt(dx2[i-N/2]) 

MSD = mean(dx2)
"""
####################################################################################
### plotting distribution of dx:
# hist(dx2, 1000, (min(dx2), max(dx2)), normed=True, histtype='step')
# hist(dx, 1000, (min(dx), max(dx)), normed=True, histtype='step')
# show()


mod_dx = [abs(dx[i]) for i in range(N)]

### computing: < dxi.dxj > 
cross = 0.0
for i in range(N-1):
    for j in range(i+1, N):
        cross += dx[i]*dx[j]


print t, '  ', MSD, '  ',  mean(dx), '  ', mean(mod_dx), '  ', 2*cross/N, '  ', N*(mean(dx))**2 - MSD  

