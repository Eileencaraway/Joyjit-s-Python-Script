import sys
import os
import StringIO
from pylab import *
from math import pi, atan2, sin, cos, sqrt, floor, exp
from matplotlib.patches import Ellipse
#from visual import * 
import numpy
from numpy import fromfile
from pylab import size
dim = 3

DOUBLE_OUTPUT=1
OUTPUT_VELOCITIES=2
OUTPUT_FORCES=4
OUTPUT_ENERGIES=8
OUTPUT_ARRAY=16
SINGLE_OUTPUT=256

class Cell:

    def __init__(self):
        self.L = []
        self.Dx = 0
        
    def computeImage(self, pos, r):
        r1 = [0.0, 0.0, 0.0]

        for d in range(3):
            m = floor(r[d]/self.L[d])
            r[d] -= m * self.L[2]
            
            dx  = [(r[d]-pos[d]), (r[d]+self.L[d]-pos[d]), (r[d]-self.L[d]-pos[d])]
            dx2  = [(r[d]-pos[d])**2, (r[d]+self.L[d]-pos[d])**2, (r[d]-self.L[d]-pos[d])**2]
            dx_2 = sorted(dx2) # sort numbers in increasing order
            
            for i in range(len(dx)):
                if dx[i]**2 == dx_2[0]:
                    r1[d] = dx[i]+pos[d]
        
        return r1
    
    def projectIntoBaseCell(self, X, Y, Z):
        N = size(X,0)
        
        for i in range(0, N):
            m = floor(Z[i]/self.L[2])
            Z[i] -= m * self.L[2]
            X[i] -= m * self.Dx
            
            m = floor(X[i]/self.L[0])
            X[i] -= m * self.L[0]
            
            m = floor(Y[i]/self.L[1])
            Y[i] -= m * self.L[1]
            
        return [X,Y,Z]
    
    def projectDispIntoBaseCell(self, dX, dY, offset):
        N = size(dX,0)

        for i in range(0, N):
            m = floor(0.5+dY[i]/self.L[1])
            dY[i] -= m * self.L[1]
            dX[i] -= m * offset
            
            m = floor(0.5+dX[i]/self.L[0])
            dX[i] -= m * self.L[0]
        
        return [dX,dY]


class ListOfAtoms:
    def __init__(self):
        self.radius = 1
        self.data = []

        
def readFile(datafile):
    
    cell = Cell()
    
    format = fromfile(datafile, int32, 1)[0]
    t = fromfile(datafile, float, 1)
    cell.L = fromfile(datafile, float, dim)
    cell.Dx = fromfile(datafile, float, 1)
    listnb = fromfile(datafile, int32, 1)
    print format, t, cell.L, cell.Dx, listnb


    if format & DOUBLE_OUTPUT:
        fmt = [('x', 'float'), ('y', 'float'), ('z', 'float')]
    else:
        if format & SINGLE_OUTPUT:
            fmt = [('x', 'float32'), ('y', 'float32'), ('z', 'float32')]
        else:
            fmt = [('x', 'longdouble'), ('y', 'longdouble'), ('z', 'longdouble')]
                
    if format & OUTPUT_VELOCITIES:
        if format & SINGLE_OUTPUT:
            fmt.append(('u', 'float32'))
            fmt.append(('v', 'float32'))
            fmt.append(('w', 'float32'))
        else:
            fmt.append(('u', 'float'))
            fmt.append(('v', 'float'))
            fmt.append(('w', 'float'))

    if format & OUTPUT_FORCES:
        if format & DOUBLE_OUTPUT:
            fmt.append(('fx', 'float'))
            fmt.append(('fy', 'float'))
            fmt.append(('fz', 'float'))
        else:
            fmt.append(('fx', 'float128'))
            fmt.append(('fy', 'float128'))
            fmt.append(('fz', 'float128'))

    
    datatype = dtype(fmt)
    print fmt

    all = []
    
    for l in range(0,listnb[0]):
        list = ListOfAtoms()
        N = fromfile(datafile, int32, 1)
        #print N
        if format & SINGLE_OUTPUT:
            list.radius = fromfile(datafile, float32, 1)[0]
        else:
            list.radius = fromfile(datafile, float, 1)[0]
            
        #print l, list.radius
        list.data = fromfile(datafile, datatype, N)
        all.append(list)


    return [cell, all, format]


def readFileAmber(datafile, No_peos, No_mms, No_lis, No_mppys, No_tfsis):
    
    cell = Cell()
    
    format = fromfile(datafile, int32, 1)[0]
    t = fromfile(datafile, float, 1)
    cell.L = fromfile(datafile, float, dim)
    cell.Dx = fromfile(datafile, float, 1)
    # listnb = fromfile(datafile, int32, 1)
    # print format, t, cell.L, cell.Dx, listnb
    print format, t, cell.L, cell.Dx


    if format & DOUBLE_OUTPUT:
        fmt = [('x', 'float'), ('y', 'float'), ('z', 'float')]
    else:
        if format & SINGLE_OUTPUT:
            fmt = [('x', 'float32'), ('y', 'float32'), ('z', 'float32')]
        else:
            fmt = [('x', 'longdouble'), ('y', 'longdouble'), ('z', 'longdouble')]
                
    if format & OUTPUT_VELOCITIES:
        if format & SINGLE_OUTPUT:
            fmt.append(('u', 'float32'))
            fmt.append(('v', 'float32'))
            fmt.append(('w', 'float32'))
        else:
            fmt.append(('u', 'float'))
            fmt.append(('v', 'float'))
            fmt.append(('w', 'float'))

    if format & OUTPUT_FORCES:
        if format & DOUBLE_OUTPUT:
            fmt.append(('fx', 'float'))
            fmt.append(('fy', 'float'))
            fmt.append(('fz', 'float'))
        else:
            fmt.append(('fx', 'float128'))
            fmt.append(('fy', 'float128'))
            fmt.append(('fz', 'float128'))

    
    datatype = dtype(fmt)
    print fmt

    all = []
    
    
    Na = fromfile(datafile, int32, 1)
    print Na # total number of atoms 
    totallist = No_peos*No_mms+No_mppys+No_tfsis+1

    for l in range(0,totallist):
        list = ListOfAtoms()
        N = fromfile(datafile, int32, 1)
        # print N
        if format & SINGLE_OUTPUT:
            list.radius = fromfile(datafile, float32, 1)[0]
        else:
            list.radius = fromfile(datafile, float, 1)[0]
            
        list.data = fromfile(datafile, datatype, N)
        all.append(list)

    return [cell, all, format]


