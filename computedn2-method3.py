#!/usr/bin/env python

import sys
import os
import StringIO
import math
import numpy
from numpy import *
#from matplotlib import *
#from pylab import show 

#####################################################################################
#####################################################################################

def computeTruePair(arr, pid, ti, tf):

    tpair = True
    p = pid+2
    count = int((tf-ti)/27)-1  # count all events
    nonpair_to_count = 0.01    # maximum ratio of non-paired events to total counts required   
    max_allowed_missing = nonpair_to_count*count
    count_missing = 0.0        # count continuous missing pairs
    #print pid, arr[ti][0], arr[tf][0], count,  
    t=ti+27

    while(t<tf):

        if arr[t][p] < 0.0001 :
            count_missing += 1.0

            if count_missing > max_allowed_missing:
                tpair = False
                break
        
        t += 27
        
    #print tpair
    return tpair

#####################################################################################
#####################################################################################

L = len(sys.argv)
if(L<3) :
    sys.stderr.write('Usage : i. filename ii. dt')
    print 
    exit()

pair = 0
carg =1
for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-pair":
            pair = 1
            carg += 1

filename = sys.argv[carg]
carg +=1
dt = float(sys.argv[carg])
carg +=1

   
os.system('~/mols/test/computedn2-method3 '+str(filename)+' '+str(dt)+'\n')
exit()

#############################################
#############################################
#############################################
#############################################
#############################################
#############################################
#############################################
#############################################
#############################################
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
l = array(List)
No_rows = len(l)
No_columns = len(l[0])
#sys.stderr.write('# nb. lines '+str(No_rows)+'\n')

#for i in range(0, No_rows):
#for j in range(0, No_columns):
#    print l[i][j],
#print
        

#################################################################################
""" computing dn2"""
#################################################################################

tot_sum = 0.0
sum_count = 0.0
tf = 27*int(dt/0.01)
#print tf, No_rows-tf

for i in range(No_rows-tf):
    for j in range(2, No_columns):
        
        if not l[i][j]==0: # li index in (j-2)th polymer at ti
            if not l[i+tf][j]==0: # li index in (j-2)th polymer at tf
                if computeTruePair(l, j-2, i, i+tf) == True:
                    tot_sum += (l[i+tf][j]-l[i][j])**2
                    sum_count += 1


print dt, " ", tot_sum/sum_count 
