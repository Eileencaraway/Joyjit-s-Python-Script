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

if(len(sys.argv)<6) :
    sys.stderr.write('Usage : -input tmin tmax dt')
    print 
    exit()

carg =1
tsave=0.01
tot_peo=0
nm_peo=0
tot_li=0
tot_mppy=0
tot_tfsi=0
for word in sys.argv[1:]:
    if word[0] == "-":

        if word == "-input":
            carg += 1
            ifile = open(sys.argv[carg])
            param = ifile.readlines()
            tot_peo  = int(param[0])
            nm_peo   = int(param[1])
            tot_li   = int(param[2])
            tot_mppy = int(param[3])
            tot_tfsi = int(param[4])
            carg +=1

        if word == "-dgamma":
            carg +=1
            tsave = float(sys.argv[carg])
            carg +=1


tmin = float(sys.argv[carg])
carg +=1
tmax = float(sys.argv[carg])
carg +=1
dt = float(sys.argv[carg])
carg +=1

###
def readIonPairs(indat, arr, tot_cats):
    data = indat.readlines()
    indat.close()

    for j in range(0, len(data)):
        
        if not (data[j].startswith("#") or data[j].startswith("\n")) :
            tmp = fromstring(data[j],sep=" ")
            
            # store values in arr      
            ln = int(floor((tmp[0]-tmin+0.000001)*tot_cats/tsave + tmp[1]));
            #print ln, tmp[0], tmp[1],  
            for c in range(2, len(tmp)):
                arr[int(tmp[c])][ln] = 1
                #print int(tmp[c]),
            
            #print 

    return 0

#################################################################################
""" reading data files Li-TFSIindex.dat and MPPY-TFSIindex.dat """
#################################################################################
tvals = int(floor((tmax-tmin+0.000001)/tsave) + 1)
tvalswli = tvals*tot_li
tvalswmy = tvals*tot_mppy

tfsiwli = [zeros(tvalswli) for i in range(tot_tfsi)]
tfsiwmy = [zeros(tvalswmy) for i in range(tot_tfsi)]
sys.stderr.write('# rows: '+str(tvalswli)+' '+str(tvalswmy)+'\n')

f1 = open('Li-TFSIindex.dat')
readIonPairs(f1, tfsiwli, tot_li)

if tot_mppy > 0:
    f2 = open('MPPY-TFSIindex.dat')
    readIonPairs(f2, tfsiwmy, tot_mppy)


#################################################################################
""" computing free and paired ions """
#################################################################################
hfli   = Histogram(-0.5, tot_li-0.5, tot_li)
hbli   = Histogram(-0.5, tot_li-0.5, tot_li)
hftfsi = Histogram(-0.5, tot_tfsi-0.5, tot_tfsi)
hbtfsi = Histogram(-0.5, tot_tfsi-0.5, tot_tfsi)
if tot_mppy > 0:
    hfmppy = Histogram(-0.5, tot_mppy-0.5, tot_mppy)
    hbmppy = Histogram(-0.5, tot_mppy-0.5, tot_mppy)

fli = pli = ftfsi = ptfsi = fmppy = pmppy = 0
count = 0.0
t = tmin
while(t<tmax-dt+0.00001):

    hfli.reset()
    hbli.reset()
    hftfsi.reset()
    hbtfsi.reset()
    if tot_mppy > 0:
        hfmppy.reset()
        hbmppy.reset()
    
    ivals = 0.0
    tit = t
    while(tit<t+dt+0.00001):

        ng_li = [0 for i in range(tot_li)] 
        ng_my = [0 for i in range(tot_mppy)] 

        tsli = int(floor((tit-tmin+0.000001)*tot_li/tsave))
        tsmy = int(floor((tit-tmin+0.000001)*tot_mppy/tsave))
        
        for i in range(tot_tfsi):

            ng_ti = 0

            for j in range(tot_li):
                
                if tfsiwli[i][tsli+j] > 0.99:
                    ng_li[j] += 1
                    ng_ti += 1

            for j in range(tot_mppy):
                
                if tfsiwmy[i][tsmy+j] > 0.99:
                    ng_my[j] += 1 
                    ng_ti += 1  
     
            if ng_ti == 0:
                hftfsi.store(i)

            if ng_ti == 1:
                hbtfsi.store(i)

        for i in range(tot_li):
            if ng_li[i] == 0:
                hfli.store(i)
            if ng_li[i] == 1:
                hbli.store(i)

        for i in range(tot_mppy):
            if ng_my[i] == 0:
                hfmppy.store(i)
            if ng_my[i] == 1:
                hbmppy.store(i)

        ivals += 1.0
        tit += tsave


    for i in range(tot_li):
        if (hfli.n[i]/ivals) > 0.9999:
            fli += 1
        if (hbli.n[i]/ivals) > 0.9999:
            pli += 1
            
    for i in range(tot_tfsi):
        if (hftfsi.n[i]/ivals) > 0.9999:
            ftfsi += 1
        if (hbtfsi.n[i]/ivals) > 0.9999:
            ptfsi += 1 

    for i in range(tot_mppy):
        if (hfmppy.n[i]/ivals) > 0.9999:
            fmppy += 1
        if (hbmppy.n[i]/ivals) > 0.9999:
            pmppy += 1
    
    count += 1.0
    t += tsave 


###
print dt, fli/tot_li/count, pli/tot_li/count,  ftfsi/tot_tfsi/count, ptfsi/tot_tfsi/count,
if tot_mppy > 0:
    print fmppy/tot_mppy/count, pmppy/tot_mppy/count,

print 


