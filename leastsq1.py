#! /usr/bin/env python

import sys
import os
import StringIO
import numpy
from math import *
from numpy import *
from pylab import *
from scipy import *
from scipy import optimize

def testfun(p,phi,gdot):
    return (0.0119/(1-phi)**p[0])*(1 + p[1]*((1-phi)**0.4)*(gdot**0.4))   

def deltaSigma(sigma,p,T,gdot):
    return -(sigma - p[0] - p[1]*gdot**0.5) 

def athermal(sigma,p,T,gdot):
     return sigma + p[2]*(-T*log(gdot/abs(p[3])))**(2.0/3.0) 


def residuals(p,y):
    err = zeros(len(y))
    for i in range(0,len(y)):
        err[i] = y[i][2] - testfun(p,y[i][1],y[i][0])
        
    return err

p0 = [2.3, 20 ]
print p0


gdotList = [0.01, 0.004, 0.001, 0.0004, 0.0001, 4e-05, 1e-05, 3e-06]
phiList = [0.89756, 0.90665, 0.91888, 0.92513, 0.92987]

gdotfile = {}
datafile = {}
data =  []
for phi in phiList:
    file = 'ph_'+str(phi)+'.dat'
    if os.path.exists(file):
        print '# Reading :', file 
        f = open(file)
        lines = f.readlines()
        
        for j in range(0, len(lines)):
            if len(lines[j])>1 and lines[j].split()[0][0] != '#':
                tmp = fromstring(lines[j],sep=" ")
                if tmp[0] in gdotList:
                    #print tmp[0], phi, tmp[1]
                    data.append([ tmp[0], phi, tmp[1] ] )

plsq = optimize.leastsq(residuals, p0, args=(data)) 
print plsq[0]


def finalerror(p,x,y,z):
    err = x - testfun(p,y,z)
    return abs(err)

gdotfile = {}
gdotList = [0.01, 0.004, 0.001, 0.0004, 0.0001, 4e-05, 1e-05, 3e-06]
phiList = [0.89756, 0.90665, 0.91888, 0.92513, 0.92987]

for phi in phiList:
    file = 'ph_'+str(phi)+'.dat'
    if os.path.exists(file):
        wfile = file+'.est'
        gdotfile[phi] = open(wfile, 'w')
        f = open(file)
        lines = f.readlines()
        f.close()
        for j in range(0, len(lines)):
            if len(lines[j])>1 and lines[j].split()[0][0] != '#':
                tmp = fromstring(lines[j],sep=" ")
                if tmp[0] in gdotList:
                    print >> gdotfile[phi], tmp[0], tmp[1], testfun(plsq[0],phi,tmp[0])

