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
dim = 2

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

    def projectIntoBaseCell(self, X, Y):
        N = size(X,0)
        
        for i in range(0, N):
            m = floor(Y[i]/self.L[1])
            Y[i] -= m * self.L[1]
            X[i] -= m * self.Dx
            
            m = floor(X[i]/self.L[0])
            X[i] -= m * self.L[0]
            
        return [X,Y]
    
    
    def projectDispIntoBaseCell(self, dX, dY, offset):
        N = size(dX,0)

        for i in range(0, N):
            m = floor(0.5+dY[i]/self.L[1])
            dY[i] -= m * self.L[1]
            dX[i] -= m * offset
            
            m = floor(0.5+dX[i]/self.L[0])
            dX[i] -= m * self.L[0]
        
        return [dX,dY]

    def correctRealPosition(self, dX, dY):
        N = size(dX,0)

        for i in range(0, N):
            m = floor(dY[i]/self.L[1])
            dX[i] += m * self.Dx
        
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

    if dim == 2:
        if format & DOUBLE_OUTPUT:
            fmt = [('x', 'float'), ('y', 'float')]
        else:
            if format & SINGLE_OUTPUT:
                fmt = [('x', 'float32'), ('y', 'float32')]
            else:
                fmt = [('x', 'longdouble'), ('y', 'longdouble')]

        if format & OUTPUT_VELOCITIES:
            if format & SINGLE_OUTPUT:
                fmt.append(('u', 'float32'))
                fmt.append(('v', 'float32'))
            else:
                fmt.append(('u', 'float'))
                fmt.append(('v', 'float'))

        if format & OUTPUT_FORCES:
            if format & DOUBLE_OUTPUT:
                fmt.append(('fx', 'float'))
                fmt.append(('fy', 'float'))
            else:
                fmt.append(('fx', 'float128'))
                fmt.append(('fy', 'float128'))

    
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


def drawAtoms(ax, X, Y, R, color='black'):

    N = size(X)
    ells = [Ellipse(xy=(X[i], Y[i]), width=2*R[i], height=2*R[i]) for i in range(0, N)]
    
    for e in ells:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_facecolor('w')
        e.set_edgecolor(color)
        e.set_alpha(0.5)
        e.set_zorder(0)


def drawAtomsWithScale(ax, X, Y, R, color='black'):

    N = size(X)
    ells = [Ellipse(xy=(X[i], Y[i]), width=2*R[i], height=2*R[i]) for i in range(0, N)]

    nb = 0
    for e in ells:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_facecolor(color)
        e.set_edgecolor('w')
        #e.set_alpha(color[nb])
        e.set_zorder(0)
        nb += 1
        
def drawAtomsMap(ax, list, data):

    N = size(data)
    emin = 0
    delta = 1 

    all=[(data[i]-emin)/delta for i in range(0, N)]
    ells = [Ellipse(xy=(float(list.data[i][0]), float(list.data[i][1])), width=2*list.radius, height=2*list.radius) for i in range(0, N)]

    for i in range(0, N):
        e = ells[i]
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_facecolor('w')
        e.set_alpha()
        e.set_zorder(0)


def center(x):
    N=size(x)
    xmean = sum(x)/N
    x -= xmean
    return x


def computeDisplacementField_mdb(cell1, cell2, list1, list2, shiftx, shifty):
    
    N = size(list1.data)
    print "Computing displacements: ", N, "atoms"
    
    dgamma = (cell2.Dx-cell1.Dx)/cell1.L[1]
    
    X1 =  [float(list1.data[i][0]) for i in range(0, N)]
    Y1 =  [float(list1.data[i][1]) for i in range(0, N)]

    X2 =  [float(list2.data[i][0]) for i in range(0, N)]
    Y2 =  [float(list2.data[i][1]) for i in range(0, N)]
    
    U =  [X2[i]-X1[i] for i in range(0, N)]
    V =  [Y2[i]-Y1[i] for i in range(0, N)]

    [U,V] = cell1.projectDispIntoBaseCell(U,V, cell2.Dx-cell1.Dx)
    U = center(U)
    V = center(V)
    [U,V] = cell1.projectDispIntoBaseCell(U,V, cell2.Dx-cell1.Dx)
    
#    print max(abs(U)), max(abs(V))
    
    return [X1,Y1,U,V]


def computeDisplacementField(cell1, cell2, list1, list2, shiftx, shifty):
    
    N = size(list1.data)
    print "Computing displacements: ", N, "atoms"
    
    dgamma = (cell2.Dx-cell1.Dx)/cell1.L[1]
    
    X1 =  [float(list1.data[i][0]) for i in range(0, N)]
    Y1 =  [float(list1.data[i][1]) for i in range(0, N)]
    cell1.correctRealPosition(X1,Y1)

    X2 =  [float(list2.data[i][0]) for i in range(0, N)]
    Y2 =  [float(list2.data[i][1]) for i in range(0, N)]
    cell2.correctRealPosition(X2,Y2)
    
    U =  [X2[i]-X1[i] - dgamma*Y1[i] for i in range(0, N)]
    V =  [Y2[i]-Y1[i] for i in range(0, N)]

    cell1.projectIntoBaseCell(X1,Y1)
    
#    [U,V] = cell1.projectDispIntoBaseCell(U,V, cell2.Dx-cell1.Dx)
#    U = center(U)
#    V = center(V)
#    [U,V] = cell1.projectDispIntoBaseCell(U,V, cell2.Dx-cell1.Dx)
    
#    print max(abs(U)), max(abs(V))
    
    return [X1,Y1,U,V]

