#!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *

verbose = False
carg    = 1
L0 = size(sys.argv)
if(L0<4) :
    sys.stderr.write('Usage : file(t0)  file(t2) cell_side')
    print 
    exit()

for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-v":
            verbose = True
            carg += 1

file1 = sys.argv[carg]
carg += 1
file2 = sys.argv[carg]
carg += 1
L = float(sys.argv[carg])
carg += 1

sys.stderr.write("# Reading files: "+file1+" and "+file2+"\n")
sys.stderr.write("# Cell side: "+str(L)+"\n")


f1 = open(file1)
data1 = f1.readlines()
f1.close()

f2 = open(file2)
data2 = f2.readlines()
f2.close()

if len(data1) != len(data2):
    exit()


for i in range(0, len(data1)):
    x0 = float(data1[i])
    x2 = float(data2[i])
    dx_20 = x2-x0    
    
    sys.stderr.write(str(x0)+" "+str(x2)+" ")
    
    if abs(dx_20) < L/2 :
        x1 = 0.5*(x0+x2)
        print '%.3f'%x1 

    else:
        m2 = int(math.floor(dx_20/abs(dx_20)))
        xp_2 = x2 - m2*L
        xp_1 = 0.5*(x0+xp_2)
        m1 = int(math.floor(xp_1/L))
        x1 = xp_1 - m1*L 
        print '%.3f'%x1 
        
    
    
