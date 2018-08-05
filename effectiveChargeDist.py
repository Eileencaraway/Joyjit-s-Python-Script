#!/usr/bin/env python

import sys
import os
import StringIO
import math
import numpy
from numpy import *
from histogram import *

#####################################################################################
#####################################################################################
"""
The script computes ratio of free ions and single paired ions from "Li-TFSIindex.dat"
and "MPPY-TFSIindex.dat" 
"""
#####################################################################################
#####################################################################################

if(len(sys.argv)<7) :
    sys.stderr.write('Usage : -input root tmin tmax dt')
    print 
    exit()

carg =1
tsave=0.01
tot_peo=0
mn_peo=0
tot_li=0
tot_mppy=0
tot_tfsi=0
rcut = 1.0
for word in sys.argv[1:]:
    if word[0] == "-":

        if word == "-input":
            carg += 1
            ifile = open(sys.argv[carg])
            param = ifile.readlines()
            tot_peo  = int(param[0])
            mn_peo  =  int(param[1])
            tot_li   = int(param[2])
            tot_mppy = int(param[3])
            tot_tfsi = int(param[4])
            carg +=1
            
        if word == "-rcut":
            carg +=1
            rcut = float(sys.argv[carg])
            carg +=1

        if word == "-dgamma":
            carg +=1
            tsave = float(sys.argv[carg])
            carg +=1


root = sys.argv[carg]
carg +=1
tmin = float(sys.argv[carg])
carg +=1
tmax = float(sys.argv[carg])
carg +=1
dt = float(sys.argv[carg])
carg +=1

hli   = Histogram(-10.5, 10.5, 21)
htfsi = Histogram(-10.5, 10.5, 21)
hmppy = Histogram(-10.5, 10.5, 21)


#################################################################################
""" distribution of effective charge """
#################################################################################
count = 0.0
t = tmin
while(t<tmax+dt):

    # reading data file charge-t-$t.dat
    fname = root+"%.2f.dat"%t
    if rcut > 1 :
        fname = root+"%.2f"%t+"-rcut-%.2f.dat"%rcut
        
    if not os.path.exists(fname):
        print 'file: ', fname, 'does not exist' 
        exit()

    f = open(fname)
    data = f.readlines()
    f.close()

    for j in range(0, len(data)):
        
        if not (data[j].startswith("#") or data[j].startswith("\n")) :
            tmp = fromstring(data[j],sep=" ")
            
            if (tmp[1]==0):
                 hli.store(tmp[3])
            if (tmp[1]==1):
                 htfsi.store(tmp[3])
            if (tmp[1]==2):
                 hmppy.store(tmp[3])


    t += dt

 
###
hli.normalize()
htfsi.normalize()
if(tot_mppy>0):
    hmppy.normalize()

if rcut > 1.0:
    ofile = open('echarge-dist-rcut-'+str(rcut)+'.dat', 'w')
else : 
    ofile = open('echarge-dist.dat', 'w')

print >> ofile, '# echarge    Li     TFSI    MPPY'

for i in range(hli.N):
    print >> ofile, i-10,   hli.rho[i],   htfsi.rho[i], 
    if(tot_mppy>0):
        print >> ofile, "   ",hmppy.rho[i],

    print >> ofile
