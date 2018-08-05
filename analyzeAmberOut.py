#! /usr/bin/env python

import sys
import os
import numpy
from numpy import *
from math import *

ar = ['TEMP(K)', 'PRESS', 'Etot', 'EKtot', 'EPtot', 'BOND', 'ANGLE', 'DIHED', '1-4NB', '1-4EEL', 'VDWAALS', 'EELEC', 'EHBOND', 'EPOLZ', 'Density']

def readFile(readfile):
    rf = open(readfile)
    data = rf.readlines()
    rf.close()

    ival=7
    if name == 'Density':
        ival=9

    i=0
    ts=0
    while (i <len(data)):
        tmp = data[i].split()
        
        if (len(tmp) > 0 and tmp[0] == 'NSTEP'):
            if(ts==0 or ts!= tmp[2]):
                print tmp[5], " ", # reading time in ps
                j=i
                while(j<i+ival) :
                    line = data[j].split()
                    for k in range(len(line)):
                        if(line[k] == name) :
                            print line[k+2] # reading the value of the given parameter e.g. EPtot
                    j +=1
                
                i=j
                ts=tmp[2]
                
        i += 1

if len(sys.argv)<3:
    sys.stderr.write("Usage: (i) ifilename (ii) one of the following numbers \n")
    for i in range(len(ar)): 
        sys.stderr.write(str(i)+" for "+ar[i]+"\n")

    print 
    exit()

carg = 1
readfile = sys.argv[carg]
carg +=1
name=ar[int(sys.argv[carg])]
carg +=1

sys.stderr.write("# reading file "+readfile+"\n")
sys.stderr.write("# reading parameter "+name+"\n")

if os.path.exists(readfile):
    readFile(readfile)
else:
    print readfile, " does not exist."


            
                


