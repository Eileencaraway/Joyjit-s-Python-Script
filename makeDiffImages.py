#! /usr/bin/env python

import sys
import os
import StringIO
import numpy
from numpy import *
from pylab import *
sys.argv

first =0
No_files =0

a = -0.05
b =  0.05

epsilon = 0
data = [numpy.empty(0),numpy.empty(0)]

count = 0
for filename in sys.argv[1:]:
    datafile = open(filename,'rb')
    Nx = fromfile(datafile, 'int32', 1)
    Ny = fromfile(datafile, 'int32', 1)
    print Nx, Ny
    data[epsilon] = fromfile(datafile, 'float32').reshape(Nx,Ny)
    datafile.close()

    data[epsilon] = data[epsilon].transpose()

    print shape(data[epsilon])
    
    if count > 0:
        data[1-epsilon] = data[epsilon]-data[1-epsilon]

        print 'Max =  ',numpy.max(data[1-epsilon])
        print 'Min =  ',numpy.min(data[1-epsilon])

        pcolor(data[1-epsilon])#,vmin=a,vmax=b)


        colorbar()
        axis('image') # make the boundary of the diagram same as data axis

        outfilename = filename+'.dif.png'
        savefig(outfilename)
        gcf().clear()
    
    
    count = count+1
    epsilon = 1-epsilon

