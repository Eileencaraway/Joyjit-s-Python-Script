#! /usr/bin/env python

import sys
import os
import StringIO
from pylab import *
from math import pi, atan2, sin, cos, sqrt, floor, exp
from matplotlib import *
from atoms import *

shift = [0.0, 0.0]
small   = True
large   = True
image   = True
verbose = False
first   = 1
embed   = 0
carg    = 1
if size(sys.argv)<2:
    sys.stderr.write("Usage: filename ")
    print
    sys.exit()

for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-v":
            verbose = True
            carg += 1

        if word == "-large":
            small = False
            carg += 1

        if word == "-small":
            large = False
            carg += 1

        if word == "-s":
            carg += 1
            shift = [float(sys.argv[carg]), float(sys.argv[carg+1])]
            carg += 2  


for filename in sys.argv[carg:]:
    
    print "Reading", filename
    datafile = file(filename,'rb')
    [cell, all, format] = readFile(datafile)
    datafile.close()
    
    if first == 1:
        first = 0
        D0 = cell.Dx

    dgamma = (cell.Dx-D0)/cell.L[1]
    
    listnb = size(all)
    print "Found ", listnb, " list(s)"
    print "Format ", format

    fig = figure(figsize=(8,8))
    fig.subplots_adjust(0,0,1,1)
    ax = fig.add_subplot(111)
    axis(ratio='exact')

    nlist = -1
    for listcount in range(size(all)):
        list = all[listcount]
        nlist += 1
        N = size(list.data)
        print N, list.radius

        Y =  [float(list.data[i][1]+shift[1]) for i in range(0, N)]
        X =  [float(list.data[i][0]+shift[0]) for i in range(0, N)]
       #X =  [float(list.data[i][0]+shift[0]-dgamma*Y[i]-0.5*(cell.Dx-cell.L[1])) for i in range(0, N)]
        R =  [float(list.radius) for i in range(0, N)]
       #cell.correctRealPosition(X,Y)
        cell.projectIntoBaseCell(X,Y)

        index = 2
        if format & OUTPUT_VELOCITIES:
            U =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            V =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1

            print "vels : ", min(U), max(U), min(V), max(V), mean(U), mean(V)
            
            if (image and listcount > 1):
                drawAtoms(ax, X, Y, R, 'red')
                quiver(X,Y,U,V)
            if (large and listcount == 0):
                drawAtoms(ax, X, Y, R)
                quiver(X,Y,U,V)
            if (small and listcount == 1):
                drawAtoms(ax, X, Y, R)
                quiver(X,Y,U,V)

        else:
            if (image and nlist > 1):
                drawAtoms(ax, X, Y, R, 'red')
            if (large and nlist == 0):
                drawAtoms(ax, X, Y, R)
            if (small and nlist == 1):
                drawAtoms(ax, X, Y, R)

            if embed == 1:
                X1 = X-cell.L[0]
                drawAtoms(ax, X1, Y, R, 'b')
                X1 = X+cell.L[0]
                drawAtoms(ax, X1, Y, R, 'b')
                Y1 = Y+cell.L[1]
                X1 = X+cell.Dx-cell.L[1]
                drawAtoms(ax, X1, Y1, R, 'b')
                X1 = X+cell.Dx
                drawAtoms(ax, X1, Y1, R, 'b')
                X1 = X+cell.Dx-2*cell.L[1]
                drawAtoms(ax, X1, Y1, R, 'b')
                Y1 = Y-cell.L[1]
                X1 = X-cell.Dx+cell.L[1]
                drawAtoms(ax, X1, Y1, R, 'b')
                X1 = X-cell.Dx
                drawAtoms(ax, X1, Y1, R, 'b')
                X1 = X-cell.Dx+2*cell.L[1]
                drawAtoms(ax, X1, Y1, R, 'b')

 
        if format & OUTPUT_FORCES:
            FX =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            FY =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            print min(FX), max(FX), min(FY), max(FY)
            #quiver(X,Y,FX,FY, color='r')

        margin = 0.4
        ax.set_xlim(-margin, cell.L[0]+margin)
        ax.set_ylim(-margin, cell.L[1]+margin)
        #ax.set_xlim(-margin-0.5* cell.L[0], 1.5*cell.L[0]+margin)
        #ax.set_ylim(-margin-0.2*cell.L[1], 1.2*cell.L[1]+margin)

axis('off')

if verbose:
    if (small and large):
            fname = filename+'.png'
            print 'Saving frame', fname
            savefig(fname)
    else:
        if large:
            fname = filename+'-large.png'
            print 'Saving frame', fname
            savefig(fname)
        if small:    
            fname = filename+'-small.png'
            print 'Saving frame', fname
            savefig(fname)
            
else:
    show()




