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
    filename = 'res.difftemperature-'+str(temperature)
    temperaturefile[temperature] = open(filename, 'w')
    
    
gdotfile = {}
for gdot in gdotlist:
    filename = 'res.diffgdot-'+str(gdot)
    gdotfile[gdot] = open(filename, 'w')

def writeFile(path, readfile, writefile):
    rf    = open(path+readfile)
    data  = rf.readlines()
    rf.close()

    wf = open(path+writefile, 'w')

    for j in range(0, len(data)):
        if not data[j].split()[0][0] == '#':
            tmp = fromstring(data[j],sep=" ")   
            print >>wf, tmp[0], tmp[1]

    return path+writefile


for temperature in temperaturelist:
    for gdot in gdotlist:
        root = 'shear-T-'+str(temperature)+'-gdot-'+str(gdot)+'-g-'
        filename1 = root+'18.dif5'
        filename2 = root+'18.dif4'
        filename3 = root+'13.dif5'
        filename4 = root+'13.dif4'
        filename5 = root+'24.dif5'
        filename6 = root+'24.dif4'
        string    = ''
        existfile = 0
        
        s =0
        while s < S:
            path = 'sys-'+str(s).zfill(3)+'/'
            
            if os.path.exists(path+filename5 or path+filename6):
                if os.path.exists(path+filename6):
                    #print path+filename2, 'exists'
                    string = string+' '+path+filename6
                else:
                    readfile  = root+'24.dif5'
                    writefile = root+'24.dif4'
                    wf = writeFile(path, readfile, writefile)
                    string = string+' '+wf 
                    
                existfile +=1
                
            elif os.path.exists(path+filename1 or path+filename2):
                if os.path.exists(path+filename2):
                    #print path+filename2, 'exists'
                    string = string+' '+path+filename2 
                else:
                    readfile  = root+'18.dif5'
                    writefile = root+'18.dif4'
                    wf = writeFile(path, readfile, writefile)
                    string = string+' '+wf 
                    
                    existfile +=1
            else:
                if os.path.exists(path+filename3 or path+filename4):
                    if os.path.exists(path+filename4):
                        #print path+filename4, 'exists'
                        string = string+' '+path+filename4 
                    else:
                        readfile  = root+'13.dif5'
                        writefile = root+'13.dif4'
                        wf = writeFile(path, readfile, writefile)
                        string = string+' '+wf 
                        
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
