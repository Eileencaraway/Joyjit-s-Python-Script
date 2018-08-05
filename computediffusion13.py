#! /usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *
from pylab import *


temperaturelist = [ 0.025, 0.05, 0.1, 0.2, 0.25, 0.3 ]
gdotlist = [ 1e-05, 4e-05, 0.0001, 0.0004, 0.001, 0.004, 0.01]
dgammalist = [0.01, 0.02, 0.04, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10.0]

carg = 1
All  = 0

if size(sys.argv)<2:
    sys.stderr.write("Usage: no of samples ")
    print
    exit()

for word in sys.argv[1:]:
    if word[0] == "-":
        
        if word == "-all":
            All   = 1
            print '# compute all '
            carg += 1

S = int(sys.argv[carg])

def computeDiff(T, gdot, s) :
    Compute = 0
    directory = 'sys-'+str(s).zfill(3)+'/'
    root = 'shear-T-'+str(T)+'-gdot-'+str(gdot)+'-g-'
    
    if os.path.exists(directory+root+'13.00.mdb'):
        Compute = 1
        if os.path.exists(directory+root+'18.00.mdb'):
            Compute = 0
  
    if Compute :
        if All :
            difffile  = directory+root+'13.dif5'
        else :
            difffile  = directory+root+'13.dif4'
                    
        if not os.path.exists(difffile) :
            if All :
                os.system('echo "# dgamma dY2 dY2_s dY2_b dR2 dR2_s dR2_b C_s C_b G_s G_b" > '+difffile)
            else :
                os.system('\\rm -f '+difffile+' && head -15 '+directory+root+'2.dif > '+difffile) 
                
            os.system('cd '+directory+'real/ ; ln -fs ../'+root+'1.00.mdb '+root+'1.00.rel ; cd -')
            
            for dgamma in dgammalist:
                if All :
                    command = '/home/chattoraj/bin_cpp/diffusion -all 1 13.0 '+str(dgamma)+' '+root+' '+directory+'real >> '+difffile
                else :
                    command = '/home/chattoraj/bin_cpp/diffusion 1 13.0 '+str(dgamma)+' '+root+' '+directory+' real >> '+difffile
                    
                os.system(command)
                     
    else:
        print directory+root+'13.00.mdb does not exist or ', directory+root+'18.00.mdb exists' 
        

s = 0
print S
while s < S:
    for T in temperaturelist:
        for gdot in gdotlist:
            computeDiff(T,gdot,s)

    s += 1
