#! /usr/bin/env python

import sys
import os
import StringIO
import numpy
from numpy import *


verbose = False
norm    = False
carg    = 1
L = size(sys.argv)
if(L<2) :
    sys.stderr.write('Usage : filename')
    print 
    exit()

for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-v":
            verbose = True
            carg += 1
        if word == "-n":
            norm = True
            carg += 1


No_files =0
for filename in sys.argv[carg:]:
    datafile = open(filename,'rb')
    Nx = fromfile(datafile, 'int32', 1)
    Ny = fromfile(datafile, 'int32', 1)
    sys.stderr.write(str(Nx)+str(Ny)+'\n')
    data = fromfile(datafile, 'float32').reshape(Nx,Ny)
    datafile.close()

    data = data.transpose()
    if norm:
        print data.min(), data.max(), mean(data), std(data)
        data = (data - mean(data))/std(data)

    sys.stderr.write('# Max, Min, Mean, Std. dev\n')
    print numpy.max(data), numpy.min(data), numpy.mean(data), numpy.std(data)
    No_files +=1


