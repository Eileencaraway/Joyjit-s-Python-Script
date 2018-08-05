#! /usr/bin/env python

import sys
import os
import StringIO
import numpy
from math import *
from numpy import *
from pylab import *
from scipy import *

def testfun1(p,T,gdot):
    return p[0] + p[1]*gdot**0.5 - p[2]*(-T*log(gdot/abs(p[3])))**(2.0/3.0)
    
def testfun(p,T,gdot):
    return p[0] + p[1]*gdot**0.5 - p[2]*(-T*(log(gdot/abs(p[3])/T**(5.0/6.0))))**(2.0/3.0)
   

def testfun3(p,T,gdot):
    return p[0] + p[1]*gdot**0.5 - p[2]*(-T*log(gdot/abs(p[3])/T**(2.0/3.0)))**(2.0/3.0)
    

def deltaSigma(sigma,p,T,gdot):
    return -(sigma - p[0] - p[1]*gdot**0.5) 

def athermal(sigma,p,T,gdot):
     return sigma + p[2]*(-T*log(gdot/abs(p[3])))**(2.0/3.0) 


def residuals(p,y):
    err = zeros(len(y))
    for i in range(0,len(y)):
        err[i] = y[i][2] - testfun(p,y[i][0],y[i][1])
        
    return err

p0 = [0.66, 2.0, 0.25, 2]
print p0


gdotList = [0.01, 0.004, 0.001, 0.0004, 0.0001, 4e-05]
tempList = [0.025, 0.05, 0.1, 0.2]

gdotfile = {}
datafile = {}
data =  []
for gdot in gdotList:
    file = 'res.gdot-'+str(gdot)+'-g-13.bin'
    if os.path.exists(file):
        print '# Reading :', file 
        f = open(file)
        lines = f.readlines()
        
        for j in range(0, len(lines)):
            if len(lines[j])>1 and lines[j].split()[0][0] != '#':
                tmp = fromstring(lines[j],sep=" ")
                if tmp[0] in tempList:
                    data.append([ tmp[0], gdot, tmp[5] ] )
                    
                                    
plsq = optimize.leastsq(residuals, p0, args=(data)) 
print plsq[0]


def finalerror(p,x,y,z):
    err = x - testfun(p,y,z)
    return abs(err)
    
gdotList = [0.01, 0.004, 0.001, 0.0004, 0.0001, 4e-05]
tempList = [0.025, 0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4]
for gdot in gdotList:
    file = 'res.gdot-'+str(gdot)+'-g-13.bin'
    if os.path.exists(file):
        wfile = file+'.est'
        gdotfile[gdot] = open(wfile, 'w')
        f = open(file)
        lines = f.readlines()
        f.close()
        for j in range(0, len(lines)):
            if len(lines[j])>1 and lines[j].split()[0][0] != '#':
                tmp = fromstring(lines[j],sep=" ")
                if tmp[0] in tempList:
                    print >> gdotfile[gdot], tmp[0], tmp[5], testfun(plsq[0],tmp[0],gdot), deltaSigma(tmp[5],plsq[0],tmp[0],gdot)#, athermal(tmp[5],plsq[0],tmp[0],gdot)#, finalerror(plsq[0],tmp[5],tmp[0],gdot) 
                
for temp in tempList:
    file = 'res.temperature-'+str(temp)+'-g-13.bin'
    if os.path.exists(file):
        wfile = file+'.est'
        out  = open(wfile, 'w')
        f = open(file)
        lines = f.readlines()
        f.close()
        for j in range(0, len(lines)):
            if len(lines[j])>1 and lines[j].split()[0][0] != '#':
                tmp = fromstring(lines[j],sep=" ")
                if tmp[0] in gdotList:
                    print >> out, tmp[0], tmp[5], testfun(plsq[0],temp,tmp[0]), deltaSigma(tmp[5],plsq[0],temp,tmp[0])#, athermal(tmp[5],plsq[0],temp,tmp[0])#, finalerror(plsq[0],tmp[5],temp,tmp[0])
        out.close()



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
