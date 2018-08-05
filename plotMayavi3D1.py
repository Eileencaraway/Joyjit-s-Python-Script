#! /usr/bin/env python

import sys
import os
import StringIO
from math import pi, atan2, sin, cos, sqrt, floor, exp
from atoms3D import *
from mayavi import mlab 

shift = [float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])]

first = 1
embed = 0

def sum2(r1, r2):
    x = 0.0
    for i in range(len(r1)):
        r = r1[i] - r2[i] 
        x += r*r
    
    return x

def drawMayavi(X, Y, Z, R, count=0):
    a = zeros(len(X), float)
    b = zeros(len(X), float)
    c = zeros(len(X), float)
    r = zeros(len(X), float)
    for i in range(0, len(X)):
        a[i] = X[i]
        b[i] = Y[i]
        c[i] = Z[i]
        r[i] = R[i]

    if count==0:
        mlab.points3d(a, b, c, r, colormap="spring", scale_factor=1)
    if count==1:
        mlab.points3d(a, b, c, r, colormap="cool", scale_factor=1)
    if count==2:
        mlab.points3d(a, b, c, r, colormap="summer", scale_factor=1)
    if count>2:
        mlab.points3d(a, b, c, r, colormap="Set3", scale_factor=1)

def drawMayaviQuiver(X, Y, Z, U, V, W, first=1):
    a = zeros(len(X), float)
    b = zeros(len(X), float)
    c = zeros(len(X), float)
    u = zeros(len(X), float)
    v = zeros(len(X), float)
    w = zeros(len(X), float)
    for i in range(0, len(X)):
        a[i] = X[i]
        b[i] = Y[i]
        c[i] = Z[i]
        u[i] = U[i]
        v[i] = V[i]
        w[i] = W[i]
    
    if first==1:
        mlab.quiver3d(a, b, c, u, v, w)
    else:
        mlab.quiver3d(a, b, c, u, v, w)

        
def drawMayavi1(X, Y, Z):
    a = zeros(len(X), float)
    b = zeros(len(X), float)
    c = zeros(len(X), float)
    for i in range(0, len(X)):
        a[i] = X[i]
        b[i] = Y[i]
        c[i] = Z[i]
        
    mlab.points3d(a, b, c, colormap="copper", scale_factor=.25)


""" for white background """
#mlab.figure(bgcolor=(1,1,1), size=(700, 700))

""" for black background """
mlab.figure(bgcolor=(0,0,0), size=(700, 700))

for filename in sys.argv[4:]:
    
    print "Reading", filename
    datafile = file(filename,'rb')
    [cell, all, format] = readFile(datafile)
    datafile.close()
    
    if first == 1:
        first = 0
        D0 = cell.Dx
        
    listnb = size(all)
    #print "Found ", listnb, " list(s)"
    #print "Format ", format

    nlist = -1
    for listcount in range(size(all)):
        list = all[listcount]
        nlist += 1
        N = size(list.data)
        #print N, list.radius
        
        if nlist == 0:
            Z =  [float(list.data[i][2]+shift[2]) for i in range(0, N)]
            Y =  [float(list.data[i][1]+shift[1]) for i in range(0, N)]
            X =  [float(list.data[i][0]+shift[0]) for i in range(0, N)]
            R =  [float(list.radius) for i in range(0, N)]
            pos_li = [float(list.data[0][0]), float(list.data[0][1]), float(list.data[0][2])]
            #cell.projectIntoBaseCell(X,Y,Z)
            #print pos_li
            drawMayavi(X, Y, Z, R, nlist)
            
        else:
            j=nlist
            while(j<4) :
                del Z[:]
                del Y[:]
                del X[:]
                del R[:]
                
                if j==3 :
                    for i in range(54*(j-1), 54*j):
                        r = [float(list.data[i][0]), float(list.data[i][1]), float(list.data[i][2])]
                        r1 = cell.computeImage(pos_li, r)
                        rcut = 3.0
                        if sum2(r1, pos_li) <= rcut**2 :
                            Z.append(r1[2]+shift[2])
                            Y.append(r1[1]+shift[1])
                            X.append(r1[0]+shift[0])
                            R.append(float(list.radius))
                    
                    if not len(R) == 0:
                        drawMayavi(X, Y, Z, R, j)
                    
                else:   
                    Z = [float(list.data[i][2]+shift[2]) for i in range(54*(j-1), 54*j)]
                    Y =  [float(list.data[i][1]+shift[1]) for i in range(54*(j-1), 54*j)]
                    X =  [float(list.data[i][0]+shift[0]) for i in range(54*(j-1), 54*j)]
                    R =  [float(list.radius) for i in range(54*(j-1), 54*j)]
                    drawMayavi(X, Y, Z, R, j)
                        
                j += 1
                
        
#mlab.outline(extent=[0.0,100.0,0.0,100.0,0.0,100.0])
mlab.view(azimuth=300, elevation=70)

fname = filename+'.png'
#print 'Saving frame', fname
#mlab.savefig(fname)

mlab.show()






