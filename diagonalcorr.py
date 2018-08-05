#! /usr/bin/env python

import sys
import os
import StringIO
import numpy
from numpy import *
from pylab import *
from matplotlib import pyplot, mpl
from scipy import fft

xcut    = False
ycut    = False
verbose = False
Lx = 1.0
carg = 1
if(size(sys.argv)<3) :
    sys.stderr.write('Usage : Lx filename')
    print 
    exit()

for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-v":
            verbose = True
            carg += 1

        if word == "-x":
            xcut = True
            carg += 1

        if word == "-y":
            ycut = True
            carg += 1

Lx = float(sys.argv[carg])
carg += 1

No_files =0
for filename in sys.argv[carg:]:
    datafile = open(filename,'rb')
    Nx = fromfile(datafile, 'int32', 1)
    Ny = fromfile(datafile, 'int32', 1)
    cg_dist = Lx/Nx
    print Nx, Ny
    data = fromfile(datafile, 'float32').reshape(Nx,Ny)
    datafile.close()

    data = data.transpose()
    print shape(data)
    
    ### diagonal correlation 
    wfile = open(filename+'.dcl', 'w')
    for i in range(0, Nx):
        print >> wfile, float(sqrt(2)*(i-Nx/2)*cg_dist), data[i][i]

    wfile.close()

    ### parallel correlation 
    if xcut:
        cx = int(Nx/2)
        xfile = open(filename+'.xcl', 'w')
        for i in range(0, Ny):
            print >> xfile, float((i-Ny/2)*cg_dist), data[cx][i]

        xfile.close()

    ### perpendicular correlation 
    if ycut:
        cy = int(Ny/2)
        yfile = open(filename+'.ycl', 'w')
        for i in range(0, Nx):
            print >> yfile, float((i-Nx/2)*cg_dist), data[i][cy]
             
        yfile.close()

    No_files +=1
