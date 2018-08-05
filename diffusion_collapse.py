#! /usr/bin/env python

import sys
import os
import numpy
from numpy import *
from math import *

if size(sys.argv)<2:
    sys.stderr.write("Usage: Temperature ")
    print
    exit()

T = sys.argv[1]
#print T
sizelist = [ 10, 20, 40, 80, 160 ]


for L in sizelist:
    #filename = '/home/joyjit/shear-thermal_data/size-'+str(L)+'/res.difftemperature-'+str(T)
    filename = '/home/joyjit/shear-thermal_data/size-'+str(L)+'/res.diffalltemperature-'+str(T)
    
    if not os.path.exists(filename):
        print filename, 'does not exist'

    else:
        print filename, 'file exists'
        f=open(filename)
        data = f.readlines()
        f.close()
        List = []
          
        for j in range(0, len(data)):
            if not data[j].split()[0] == '#':
                tmp = fromstring(data[j],sep=" ")
                List.append(tmp)


        #diff_file = 'diffcollapse-'+str(T)+'-L-'+str(L)
        diff_file = 'diffallcollapse-'+str(T)+'-L-'+str(L)
        tempfile = open(diff_file, 'w')
        print >> tempfile, '#column->gdot(0.01, 0.004, 0.001, 0.0004, 0.0001)+ diff error'

            
        for line in List:
            #print >> tempfile, (line[0]**0.5)*L, ' ', line[1]/L,  line[2]/L, 
            print >> tempfile, (line[0]**0.5)*L, ' ', line[1]/L, ' ', line[2]/L, ' ', line[3]/L, ' ', line[4]/L,  line[5]/L, ' ', line[6]/L,  
            print >> tempfile


#os.system('bxy 1:2 diffcollapse-T-'+str(T)+'-L-10 diffcollapse-T-'+str(T)+'-L-20 diffcollapse-T-'+str(T)+'-L-40 diffcollapse-T-'+str(T)+'-L-80 diffcollapse-T-'+str(T)+'-L-160 ')
#os.system('rm -rf diffcollapse-'+str(T)+'L-* ')


