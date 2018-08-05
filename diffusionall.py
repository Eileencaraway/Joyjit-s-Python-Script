#! /usr/bin/env python

import sys
import os
import numpy
from numpy import *
from math import *

if size(sys.argv)<2:
    sys.stderr.write("Usage: no of samples ")
    print
    exit()

S = int(sys.argv[1])
#print S

temperaturelist = [ 0.025, 0.05, 0.1, 0.2, 0.25, 0.3 ]
gdotlist = [ 0.01, 0.004, 0.001, 0.0004, 0.0001, 4e-05, 1e-05 ]

temperaturefile = {}
for temperature in temperaturelist:
    filename = 'res.diffalltemperature-'+str(temperature)
    temperaturefile[temperature] = open(filename, 'w')
    print >>temperaturefile[temperature], "# gdot dY2 dY2_s dY2_b dR2 dR2_s dR2_b C_s C_b G_s G_b"

    
gdotfile = {}
for gdot in gdotlist:
    filename = 'res.diffallgdot-'+str(gdot)
    gdotfile[gdot] = open(filename, 'w')
    print >>gdotfile[gdot], "# T dY2 dY2_s dY2_b dR2 dR2_s dR2_b C_s C_b G_s G_b"

for temperature in temperaturelist:
    for gdot in gdotlist:
        root      = 'shear-T-'+str(temperature)+'-gdot-'+str(gdot)+'-g-'
        filename  = root+'13.dif5'
        filename2 = root+'18.dif5'
        filename3 = root+'24.dif5'
        string    = ''
        existfile = 0
        s         = 0

        while s < S:
            path = 'sys-'+str(s).zfill(3)+'/'

            if os.path.exists(path+filename3):
                # print path+filename2, 'exists'
                string = string+' '+path+filename3 
                existfile +=1
            else:
                if os.path.exists(path+filename2):
                    # print path+filename2, 'exists'
                    string = string+' '+path+filename2 
                    existfile +=1
                else:
                    if os.path.exists(path+filename):
                        # print path+filename, 'exists'
                        string = string+' '+path+filename 
                        existfile +=1

            s +=1
            
        if existfile > 0:
            os.system('~/pythontest/avg_cutoff-diff.py '+string[0:]+' > look')
            file = open('look')
            data = file.readlines()

            if len(data)> 0:
                vals = data[len(data)-1].split() 
                
                if len(vals) > 4:
                    print >>gdotfile[gdot], temperature, 
                    print >>temperaturefile[temperature], gdot, 
                        
                for i in range(6, len(vals)):
                    print >>gdotfile[gdot], vals[i],
                    print >>temperaturefile[temperature], vals[i],
                        
                print >>gdotfile[gdot]
                print >>temperaturefile[temperature]
                
            os.system('rm -rf look')
