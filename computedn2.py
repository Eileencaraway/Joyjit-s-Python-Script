#!/usr/bin/env python

import sys
import os
import StringIO
import math
import numpy
from numpy import *
#from matplotlib import *
#from pylab import show 


L = size(sys.argv)
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
#print tf

for i in range(No_rows-tf):
    for j in range(2, No_columns):
        
        if not l[i][j]==0: # li index in (j-2)th polymer at ti
            if not l[i+tf][j]== 0: # li index in (j-2)th polymer at tf
                tot_sum += (l[i+tf][j]-l[i][j])**2
                sum_count += 1


print dt, " ", tot_sum/sum_count 

"""
for i in range(No_rows-tf):
    n = zeros(10, 'f')
    ts = 0
    while (ts-1 < int(dt/0.01)) :
        for j in range(2, No_columns):
            if not l[i+27*ts][j]==0: # li index in (j-2)th polymer at ti
                n[j-2] += 1 
        
        ts += 1

    for nb in range(10):
        if n[nb] == (1+int(dt/0.01)): # li index in (j-2)th polymer at tf
            tot_sum += (l[i+tf][nb+2]-l[i][nb+2])**2
            sum_count += 1


print dt, " ", tot_sum/sum_count 
"""
