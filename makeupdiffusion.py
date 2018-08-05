#! /usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *
from pylab import *

L = size(sys.argv)
if(L<2) :
    sys.stderr.write('Usage : No_system ')
    print 
    exit()
    
smax = int(sys.argv[1])
temperaturelist = [ 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.35, 0.4, 0.5, 0.6 ]
gdotlist = [ 0.01, 0.004, 0.001, 0.0004, 0.0001 ]
dgammalist = [8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10]


for T in temperaturelist:
    for gdot in gdotlist:
        for s in range(0,smax):
            filename = 'shear-T-'+str(T)+'-gdot-'+str(gdot)+'-g-13.dif4'
            
            if os.path.exists('sys-'+str(s).zfill(3)+'/'+filename):
                file = open('sys-'+str(s).zfill(3)+'/'+filename)
                data = file.readlines()
                file.close()
                if len(data)< 118:
                    sys.stderr.write('sys-'+str(s).zfill(3)+'/'+filename+'\n')
                    os.chdir('sys-'+str(s).zfill(3))
                    for dgamma in dgammalist:
                        os.system('/home/chattoraj/cppsample/diffusionLJ 1 13.0 ' +str(dgamma)+' shear-T-'+str(T)+'-gdot-'+str(gdot)+'-g- real >> '+filename)
                        
                    os.chdir('..')
                        
