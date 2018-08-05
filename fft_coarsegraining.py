#! /usr/bin/env python

import sys
import os
import StringIO
import numpy
from numpy import *
from pylab import *
#from scipy import *


L = size(sys.argv)
if(L<4) :
    sys.stderr.write('Usage : Min, ' 'Max, ' ' filename')
    print 
    exit()

a = float(sys.argv[1])
b = float(sys.argv[2])
#print a, b
first =0
No_files =0
for filename in sys.argv[3:]:
    datafile = open(filename,'rb')
    Nx = fromfile(datafile, 'int32', 1)
    Ny = fromfile(datafile, 'int32', 1)
    print Nx, Ny
    data = fromfile(datafile, 'float32').reshape(Nx,Ny)
    datafile.close()

    data = data.transpose()
    print shape(data)
    if first==0:
        first_data = data
        first = 1
    print 'Max =  ',numpy.max(data)
    print 'Min =  ',numpy.min(data)
    print 'Mean = ',numpy.mean(data)
    No_files +=1
    fftdata = fft2(data)
    print 'Max =  ',numpy.max(abs(fftdata))
    print 'Min =  ',numpy.min(abs(fftdata))
    print 'Mean = ',numpy.mean(abs(fftdata))
#    print fftdata

#if No_files>1:
#    data -= first_data 
#    print 'Max =  ',numpy.max(data)
#    print 'Min =  ',numpy.min(data)
#    print 'Mean = ',numpy.mean(data)
    
pcolor(abs(fftdata))
#pcolor(abs(fftdata),vmin=a,vmax=b)
#axis('image')   #make the boundary of the diagram same as data axis
#clim(-6.0,6.0)
colorbar()
#savefig(filename+'.png')
show()    


