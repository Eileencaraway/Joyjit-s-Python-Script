#! /usr/bin/env python

import sys
import os
import StringIO
import numpy
from math import *
from numpy import *
from pylab import *
from scipy import optimize

def testfun(p,y0):
    gt = 0.0
    for m in range(1, N):
        #gt += (1 - exp(-y0*m**2/p[1]))/m/m
        gt += (1 - exp(-y0*m**2/p[0]))/m/m

    #return gt*2*p[0]*p[0]/pi/pi
    #return gt*2*15.04*15.04/pi/pi  # set Re^2 values 
    #return gt*2*9.67*9.67/pi/pi  # set Re^2 values 
    return gt*2*22.7*22.7/pi/pi  # set Re^2 values 
    #return gt*2*40.0*40.0/pi/pi  # set Re^2 values 

def residuals(p,y):
    err = zeros(len(y))
    for i in range(0,len(y)):
        err[i] = y[i][1] - testfun(p,y[i][0])
        
    return err


#####################################################################################
#####################################################################################
"""
The script performs least square fittings ...
"""
#####################################################################################
#####################################################################################

if(len(sys.argv)<6) :
    sys.stderr.write("Usage : i. nb of datafiles, ii. datafiles\n")
    sys.stderr.write("      : column number of iii. independent variable, iv. dependent variable ")
    sys.stderr.write("      : iv. approx. values of Re and tau ")
    print 
    exit()

N = 54
carg =1
for word in sys.argv[1:]:
    if word[0] == "-":

        if word == "-N":
            carg += 1
            N = int(sys.argv[carg])
            print "# number of monomers: ", N
            carg += 1


nb_dfiles = int(sys.argv[carg])
carg += 1
datafiles = []
for i in range(nb_dfiles):
    datafiles.append(sys.argv[carg])
    carg += 1

indv = int(sys.argv[carg])
carg += 1
dv = int(sys.argv[carg])
carg += 1
p0 = []
while carg < len(sys.argv):
    p0.append(float(sys.argv[carg]))
    carg += 1
print '# supplied values:', p0


################################################################################
"""  reading data from datafiles """
################################################################################
data =  []

for df in datafiles:
    if os.path.exists(df):
        print '# Reading :', df 
        f = open(df)
        lines = f.readlines()
        
        for j in range(0, len(lines)):
            if len(lines[j])>1 and lines[j].split()[0][0] != '#':
                tmp = fromstring(lines[j],sep=" ")
                data.append([tmp[indv], tmp[dv]])
                    
                                    
plsq = optimize.leastsq(residuals, p0, args=(data)) 
print "# new values: ", plsq[0]

for i in range(len(data)):
    print data[i][0], data[i][1], testfun(plsq[0],data[i][0])
                

