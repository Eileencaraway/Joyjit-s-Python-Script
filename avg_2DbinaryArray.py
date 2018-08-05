#! /usr/bin/env python

import sys
import os
from numpy import *
import StringIO
from math import pi, atan2, sin, cos, sqrt, floor, exp
pathdir = os.environ['HOME']+'/lammps-9Dec14/analysis_code/'
sys.path.append(pathdir) 
from coarseGraining import *

chngsign= False

######################################
def readFile(filename, normalize, norm):
    datafile = open(filename,'rb')
    Nx = fromfile(datafile, 'int32', 1)
    Ny = fromfile(datafile, 'int32', 1)
    #print Nx, Ny
    data = fromfile(datafile, 'float32').reshape(Nx,Ny)
    datafile.close()

    if chngsign:
        data = -1.0*data

    print data.min(), data.max(), mean(data), std(data)
    if normalize:
            print norm0
            data /= norm0/10000

    if norm:
        data = (data - mean(data))/std(data)
        print data.min(), data.max(), mean(data), std(data)

    return data
######################################


######################################
def sliceData(darray, x0, x1, y0, y1):
    n=[(x1-x0+1), (y1-y0+1)]
    narray=zeros(n)
    
    for i in range(n[0]):
        for j in range(n[1]):
            narray[i][j] = data[x0+i][y0+j]
            
    return narray
######################################
    
min=-0.000015 
max=0.000032
normalize = False
norm      = False 
sliced    = False
px=1
py=1
carg = 1

if(size(sys.argv)<2):
    sys.stderr.write('Usage : binary files\n')
    exit()

for word in sys.argv[1:]:
    if word[0] == "-":
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

        if word == "-n":
            norm = True
            carg += 1

        if word == "-csign":
            chngsign = True  
            carg += 1
        
        if word == "-slice":
            sliced = True
            carg += 1
            px = float(sys.argv[carg]) # the sliced amount (in fraction) along x 
            carg += 1
            py = float(sys.argv[carg]) # the sliced amount (in fraction) along y 
            carg += 1


nb_files = 0
for filename in sys.argv[carg:]:
    if not os.path.exists(filename):
        continue

    print '***', filename
    data   = readFile(filename, normalize, norm)
    pixels = shape(data)
    print pixels
    if nb_files==0:
        pfirst=pixels
        sum_data = zeros(pixels)

    xl=0
    xh=pixels[0]
    yl=0
    yh=pixels[1]

    if sliced:
        xl=int(0.5*pixels[0]*(1-px))
        xh=int(pixels[0] - 0.5*pixels[0]*(1-px))
        yl=int(0.5*pixels[1]*(1-py))
        yh=int(pixels[1] - 0.5*pixels[1]*(1-py))
        print xl, xh, yl, yh
        data = sliceData(data, xl, xh, yl, yh)

    if pixels==pfirst:
        sum_data += data
        nb_files += 1

avg_data = sum_data/nb_files
print avg_data.min(), avg_data.max(), mean(avg_data), std(avg_data)
writeBinary(avg_data, 'avg_data')
"""
for i in range(pfirst[0]):
    for j in range(pfirst[1]):
"""
