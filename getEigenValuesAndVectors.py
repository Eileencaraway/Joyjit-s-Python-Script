#! /usr/bin/env python

import sys
import os
import StringIO
import numpy as np

##################################################################################
#                 !!! Attention !!! 
# this function will only work for: 
# i.   2x2 matrix
# ii.  all the matrix elements which are real  
# iii. two off diagonal elements which have the same sign  
##################################################################################
def getEigenValsVectors(a):
    b=0.5*(a[0][0]+a[1][1])
    c=0.5*np.sqrt((a[0][0]-a[1][1])**2+4*a[0][1]*a[1][0])
    evals = [b+c, b-c]
    
    if evals[0]==0 and evals[1]==0:
        if a[0][0]==0:
            return [0,0], [1,0], [0,1] 
        else:
            return [0,0], [0.7071067812,0.7071067812], [0.7071067812,0.7071067812] 
        
    if a[0][1]==0:
        if a[0][0]==evals[0]:
            evec0 = [1, 0]
            evec1 = [0, 1]
        else:
            evec0 = [0, 1]
            evec1 = [1, 0]
            """
            if a[1][0]==0:
                evec1 = [1, 0]
            else:
                b0    = 1
                b1    = -(a[1][1]-evals[1])/a[1][0]
                norm  = np.sqrt(b0*b0+b1*b1) 
                evec1 = [b0/norm, b1/norm]
            """
        return evals, evec0, evec1 
        
    a0    = 1
    a1    = -(a[0][0]-evals[0])/a[0][1]
    norm  = np.sqrt(a0*a0+a1*a1) 
    evec0 = [a0/norm, a1/norm]
    b0    = 1
    b1    = -(a[0][0]-evals[1])/a[0][1]
    norm  = np.sqrt(b0*b0+b1*b1) 
    evec1 = [b0/norm, b1/norm]
    return evals, evec0, evec1 


s = np.random.random((2,2))
s[0][0]=1
s[0][1]=-1
s[1][0]=1
s[1][1]=3
print s 

evals, evecs = np.linalg.eig(s)
print evals, evecs.transpose()

evals, evec0, evec1   = getEigenValsVectors(s)
print evals, evec0, evec1

