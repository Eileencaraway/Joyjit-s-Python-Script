#! /usr/bin/env python

import sys
import os
import StringIO
from math import pi, atan2, sin, cos, sqrt, floor, exp
from atoms3D import *
from mayavi import mlab 

#colrlist = ["spring", "cool", ""]

def drawMayavi(X, Y, Z, R, first=1):
    a = zeros(len(X), float)
    b = zeros(len(X), float)
    c = zeros(len(X), float)
    r = zeros(len(X), float)
    for i in range(0, len(X)):
        a[i] = X[i]
        b[i] = Y[i]
        c[i] = Z[i]
        r[i] = R[i]
    
    if first==0:
        mlab.points3d(a, b, c, r, colormap="spring", scale_factor=1)
    if first==1:
        mlab.points3d(a, b, c, r, colormap="cool", scale_factor=1)
    if first > 1:
        mlab.points3d(a, b, c, r, colormap="autumn", scale_factor=1)


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

        
#####################################################################################
#####################################################################################

shift = [0.0, 0.0, 0.0]
first = 1

if(size(sys.argv)<2) :
    sys.stderr.write('Usage : i. filename(s)')
    print 
    exit()

carg =1
for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-s":
            carg += 1
            for i in range(3):
                shift[i] = [float(sys.argv[carg])]
                carg += 1
            print shift 

#################################################################################
""" reading files """
#################################################################################
for filename in sys.argv[carg:]:
    
    print "Reading", filename
    datafile = file(filename,'rb')
    [cell, all, format] = readFile(datafile)
    datafile.close()
    
    if first == 1:
        first = 0
        D0 = cell.Dx
        
    listnb = size(all)
    print "Found ", listnb, " list(s)"
    print "Format ", format

    nlist = -1
    for listcount in range(size(all)):
        list = all[listcount]
        nlist += 1
        N = size(list.data)
        print N, list.radius
        
        Z =  [float(list.data[i][2]+shift[2]) for i in range(0, N)]
        Y =  [float(list.data[i][1]+shift[1]) for i in range(0, N)]
        X =  [float(list.data[i][0]+shift[0]) for i in range(0, N)]
        R =  [float(list.radius) for i in range(0, N)]
        cell.projectIntoBaseCell(X,Y,Z)

        index = 3
        if format & OUTPUT_VELOCITIES:
            U =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            V =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            W =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1

            print "vels : ", min(U), max(U), min(V), max(V), min(W), max(W)
            
            #if listcount >= 1:
                #print listcount 
                #drawMayavi(X, Y, Z, R, listcount)
                #drawMayaviQuiver(X,Y,Z,U,V,W)
            #else:
                #print listcount, " drawing quiver " 
                #drawMayaviQuiver(X,Y,Z,U,V,W)
                #drawMayavi(X, Y, Z, R, listcount)
            
            drawMayavi(X, Y, Z, R, listcount)
            drawMayaviQuiver(X,Y,Z,U,V,W)

        else:
            #if nlist <= 1:
            drawMayavi(X, Y, Z, R, nlist)
 
 
        if format & OUTPUT_FORCES:
            FX =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            FY =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            FZ =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1

            print min(FX), max(FX), min(FY), max(FY), min(FZ), max(FZ)

            #quiver(X,Y,FX,FY, color='r')

        
#mlab.outline()

fname = filename+'.png'
#print 'Saving frame', fname
#mlab.savefig(fname)
mlab.show()






