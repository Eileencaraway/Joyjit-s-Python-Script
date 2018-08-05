#! /usr/bin/env python

import sys
import os
import StringIO
from math import pi, atan2, sin, cos, sqrt, floor, exp
from matplotlib import *
import numpy as np
from atoms import *

shift = [0.0, 0.0]
small   = True
large   = True
image   = True
verbose = False
min=-1.0 
max=1.0
normalize = False
carg    = 1

if size(sys.argv)<3:
    sys.stderr.write("Usage: i. configure filename ii. observable filename [1D array]")
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

        if word == "-shift":
            carg += 1
            shift = [float(sys.argv[carg]), float(sys.argv[carg+1])]
            carg += 2  
        
        if word == "-set":
            carg += 1
            min = float(sys.argv[carg])
            carg += 1
            max = float(sys.argv[carg])
            carg += 1
            print min, max

        if word == "-norm":
            normalize = True
            carg += 1
            norm0 = float(sys.argv[carg])
            carg += 1
            print norm0


filename = sys.argv[carg]
carg += 1
observable = sys.argv[carg]
carg += 1


###
ofile = open(observable,'rb')
Nx = fromfile(ofile, 'int32', 1)
print Nx
odata = fromfile(ofile, 'float')
ofile.close()
"""
for i in range(len(odata)):
    print odata[i],
print
""" 
print np.max(odata), np.min(odata)


###
print "Reading", filename
datafile = file(filename,'rb')
[cell, all, format] = readFile(datafile)
datafile.close()

listnb = size(all)
print "Found ", listnb, " list(s)"
print "Format ", format

X=[]
Y=[]
R=[]
area=[]
nlist = -1
for listcount in range(size(all)):
    list = all[listcount]
    nlist += 1
    N = size(list.data)
    
    y =  [float(list.data[i][1]+shift[1]) for i in range(0, N)]
    x =  [float(list.data[i][0]+shift[0]) for i in range(0, N)]
    r =  [float(list.radius) for i in range(0, N)]
    cell.projectIntoBaseCell(x,y)
    
    for i in range(len(y)):
        X.append(x[i])
        Y.append(y[i])
        R.append(r[i])
        area.append(100*pi*r[i]*r[i])


###        
fig = figure(figsize=(8,8))
fig.subplots_adjust(0,0,1,1)
ax = fig.add_subplot(111)
axis(ratio='exact')
#axis('off')
marginx = 8.5
marginy = 8.5
ax.set_xlim(-marginx, cell.L[0]+marginx)
ax.set_ylim(-marginy, cell.L[1]+marginy)

image = ax.scatter(X, Y, c=odata, s=area, alpha=0.75, cmap=cm.jet, vmin=min, vmax=max)
cax = fig.add_axes([0.07, 0.1, 0.02, 0.8])
fi = fig.colorbar(image,cax)
cax.yaxis.set_ticks_position('left')


if verbose:
    fname = filename+'.png'
    print 'Saving frame', fname
    savefig(fname)
else:
    show()




