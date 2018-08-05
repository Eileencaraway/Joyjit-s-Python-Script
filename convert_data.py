#!/usr/bin/env python
#reading data from .dat file
#convert data file into two files called .hdr and .bin 
import sys
import os
import math
import numpy
from numpy import *
import struct
from pylab import *

sys.argv
no_column = int(sys.argv[1]) #no of columns of the .dat file 
first=1

for filename in sys.argv[2:]:
    f = open(filename)
    data = f.readlines()
    hdr= open(filename+'.hdr', 'w')
    bin= open(filename+'.bin', 'wb')
    bin.write(struct.pack('i',no_column))
    for j in range(0, len(data)):
        if data[j].split()[0] == '#':
            hdr.write(data[j])
        else:
            bin.write(fromstring(data[j],sep=" "))
    sys.stderr.write('import '+filename+' size-'+str(len(data))+'\n')
    f.close()
    
    print '#no_column=',no_column




    
