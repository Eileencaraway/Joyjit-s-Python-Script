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
The script computes the time duration td of a cation and an anion. 
It reads information from "Li-TFSIindex.dat" or "MPPY-TFSIindex.dat" 

"""
#####################################################################################
#####################################################################################

if(len(sys.argv)<5) :
    sys.stderr.write('Usage : i. nb. cations ii. nb. anions iii. filename iii. dt')
    print 
    exit()

carg =1
"""
tot_peo=0
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
            tot_li   = int(param[1])
            tot_mppy = int(param[2])
            tot_tfsi = int(param[3])
            carg +=1
"""
tot_cations = int(sys.argv[carg])
carg +=1
tot_anions  = int(sys.argv[carg])
carg +=1
filename    = sys.argv[carg]
carg +=1
dt = float(sys.argv[carg])
carg +=1

###
def searchMore(anioni, time, tot):

    nopair = False
    t1 = time+tot_cations
    if t1 < tot : 
        if anioni[t1] == 0.0:
            t2 = time+2*tot_cations
            if t2 < tot :
                if anioni[t2] == 0.0:
                    nopair = True

            else :
                nopair = True
    else :
        nopair = True


    return nopair

#################################################################################
""" reading data file """
#################################################################################
f = open(filename)
data = f.readlines()
f.close()
List = []
for j in range(0, len(data)):
    if not (data[j].startswith("#") or data[j].startswith("\n")) :
            tmp = fromstring(data[j],sep=" ")
            #print len(tmp)
            List.append(tmp)
            
sys.stderr.write('# import '+filename+' size-'+str(len(List))+'\n')

"""
for i in range(len(List)):
    if List[i][1]==1:
        print List[i][0],
        for j in range(2, len(List[i])):
            print List[i][j],
    #print
print 
"""

#################################################################################
""" rearranging data as column matrices """
#################################################################################
ti = List[0][0]
tf = List[len(List)-1][0]
tvals = floor((tf-ti+0.000001)/dt) + 1 
tvals = tvals*tot_cations
sys.stderr.write(str(ti)+' '+str(tf)+' '+str(tvals)+'\n')
                
tfsis = [zeros(tvals) for i in range(tot_anions)]

for l in range(len(List)):
    rows = floor( (List[l][0]-ti+0.000001)*tot_cations/dt + List[l][1] )
    #print List[l][0], List[l][1], dt, rows 
    
    for c in range(2, len(List[l])):
        tfsis[ int(List[l][c]) ][rows] = 1.0 
        
"""
t=1
while(t<tvals):
    if tfsis[7][t]==1:
        print t, tfsis[7][t], 
    t += tot_cations
print 
"""

#################################################################################
""" computing pair duration """
#################################################################################
min  = 0.0
max =  10.01
ival = 1001
hist = Histogram(min, max, ival)
tot_sum = 0.0
tot_sum2 = 0.0
sum_count = 0.0

for i in range(tot_anions):
    for li in range(tot_cations):
        
        t=li
        #print '## ', t, ':'
        while(t<tvals):
            if tfsis[i][t] == 1.0:
                t1 = t+tot_cations
                
                while(t1<tvals):
                  
                    if tfsis[i][t1] == 0.0:
                        if searchMore(tfsis[i], t1, tvals):
                            tau = (t1-tot_cations-t)*dt/tot_cations
                            tot_sum += tau
                            tot_sum2 += tau*tau
                            sum_count += 1
                            hist.store(tau)
                            #print i, t1, t, tau 
                            t = t1
                            break 
                        
                
                    t1 += tot_cations

            t += tot_cations 

        #print 


#################################################################################
""" writing information """
#################################################################################
pout = open(filename+".tau", 'w')
print >> pout, '# Reading filename: ',filename
print >> pout, '# tmin tmax = ', ti,' ',tf
 
tau = tot_sum/sum_count
error =  sqrt((tot_sum2/sum_count) - (tot_sum/sum_count)**2)
print >> pout, '# nb. of events = ', sum_count 
print >> pout, '# tau = ', tau,'ns' 

hist.normalize()
for i in range(hist.N):
    print >> pout, i*hist.dx+min, " ", hist.rho[i]

pout.close()
sys.stderr.write('!! Done !! \n')
