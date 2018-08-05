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
    return p[0]*exp(-4660*y0/1000.0)    

def deltaSigma(sigma,p,T,gdot):
    return -(sigma - p[0] - p[1]*gdot**0.5) 

def athermal(sigma,p,T,gdot):
     return sigma + p[2]*(-T*log(gdot/abs(p[3])))**(2.0/3.0) 


def residuals(p,y):
    err = zeros(len(y))
    for i in range(0,len(y)):
        err[i] = y[i][1] - testfun(p,y[i][0])
        # err[i] = y[i][2] - testfun(p,y[i][0],y[i][1])
        
    return err


#####################################################################################
#####################################################################################
"""
The script computes ...
"""
#####################################################################################
#####################################################################################

if(len(sys.argv)<6) :
    sys.stderr.write("Usage : i. nb of datafiles, ii. datafiles\n")
    sys.stderr.write("      : columns of iii. independent variable, iv. dependent variable ")
    sys.stderr.write("      : iv. approx. values of parameters ")
    print 
    exit()

carg =1
for word in sys.argv[1:]:
    if word[0] == "-":

        if word == "-input":
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
print '#',p0


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
print "#", plsq[0]

"""
def finalerror(p,x,y,z):
    err = x - testfun(p,y,z)
    return abs(err)
"""
def finalerror(p,x,y):
    err = x - testfun(p,y)
    return abs(err)
    
for i in range(len(data)):
    print data[i][0], data[i][1], testfun(plsq[0],data[i][0])#, deltaSigma(tmp[5],plsq[0],tmp[0],gdot)#, athermal(tmp[5],plsq[0],tmp[0],gdot)#, finalerror(plsq[0],tmp[5],tmp[0],gdot) 
                

#pf = plsq[0]
#print pf
#x = zeros(len(data))
#sigma = zeros(len(data))
#sigma_estimated = zeros(len(data))
#for i in range(0,len(data)):
        #x[i] = data[i][0]
        #sigma[i] = data[i][2]
        #sigma_final[i] = pf[0]+pf[1]*data[i][1]**0.5 - pf[2]*(-data[i][0]*log(data[i][1]/pf[3]))**(2.0/3.0)  

#plot(x,sigma,'r--',x,sigma_estimated,'b')
#legend(['RealData', 'EstimatedData'])  
#show()
