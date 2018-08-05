#!/usr/bin/env python

import sys
import os
import StringIO
import numpy
from numpy import *

L = size(sys.argv)
if(L<2) :
    sys.stderr.write('Usage : no. of systems ')
    print 
    exit()

N = int(sys.argv[1])


temperaturelist = [ 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.3 ]
gdotlist = [0.0001, 0.0004, 0.001, 0.004, 0.01 ]


temperaturefile = {}
for temperature in temperaturelist:
    filename = 'res.stressdistn-T-'+str(temperature)
    temperaturefile[temperature] = open(filename, 'w')

    
gdotfile = {}
for gdot in gdotlist:
    filename = 'res.stressdistn-gdot-'+str(gdot)
    gdotfile[gdot] = open(filename, 'w')

for gdot in gdotlist:
    for T in temperaturelist:
        filename  = 'shear-T-'+str(T)+'-gdot-'+str(gdot)+'.dis'+str(N)
        if not os.path.exists(filename):
            command = '/home/chattoraj/cppsample/analyzeStress -sys '+str(N)+' shear-T-'+str(T)+'-gdot-'+str(gdot)+'-g- 2 13 0.01 .rel > '+filename
            os.system(command)
            file = open(filename)
            data = file.readlines()
            file.close()
            val = data[0].split()
            if len(val)>0:
                print >> gdotfile[gdot], T,
                print >> temperaturefile[T], gdot,
                for i in range(0, len(val)):
                    print >> gdotfile[gdot], val[i],
                    print >> temperaturefile[T], val[i],

                print >> gdotfile[gdot]
                print >> temperaturefile[T]
                            
