#! /usr/bin/env python

import sys
import os
import numpy
from numpy import *


sizelist = [ 10, 20, 40, 80 ]
temperaturelist = [ 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 ]
gdotlist = [1e-05, 4e-05, 0.0001, 0.0004, 0.001, 0.004, 0.01]


for gdot in gdotlist:
    first =1

    for L in sizelist:
        filename = '~/shear-therma_data/size-'+str(L)+'/res.diff_gdot-'+str(gdot)

        if not os.path.exists(filename):
            print filename, 'does not exist'

        else:
            print filename, 'file exists'

            if first == 1:
                diff_file = 'diffusion_L-gdot-'+str(gdot)
                tempfile = open(diff_file, 'w')
                first=0

            f=open(filename)
            data = f.readlines()
            f.close()
            List = []
            print >> tempfile, L,
            for j in range(0, len(data)):
                tmp = fromstring(data[j],sep=" ")
                List.append(tmp)

            
            for i in range(0,len(List)):
                print List[i][0],  List[i][1]
                print >> tempfile, List[i][1], 
                
            print >> tempfile




for T in temperaturelist:
    first = 1
    for L in sizelist:
        filename = '~/shear-thermal_data/size-'+str(L)+'/res.diff_temp-'+str(T)
        if not os.path.exists(filename):
            print filename, 'does not exist'
        else:
            print filename, 'file exists'
            if first == 1:
                diff_file2 = 'diffusion_L-temp-'+str(T)
                gdotfile = open(diff_file2, 'w')
                first=0

            f=open(filename)
            data = f.readlines()
            f.close()
            List = []
            print >> gdotfile, L,
            for j in range(0, len(data)):
                tmp = fromstring(data[j],sep=" ")
                List.append(tmp)
                    
            
            for i in range(0,len(List)):
                print List[i][0],  List[i][1]
                print >> gdotfile, List[i][1], 
                
            print >> gdotfile
