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
tot1 = 0.0
sum_count1 = 0.0
tot2 = 0.0
sum_count2 = 0.0
tf = 27*int(dt/0.01)
#print tf

for i in range(No_rows-tf):
    dni = []
    for j in range(2, No_columns):
        if not l[i][j]==0: # li index in (j-2)th polymer at ti
            if not l[i+tf][j]==0: # li index in (j-2)th polymer at tf
                diff = l[i+tf][j]-l[i][j]
                dni.append(diff)
          
    if len(dni)==1:
        s =  dni[0]**2
        tot1 += s
        sum_count1 += 1

        tot_sum += s
        sum_count += 1

    if len(dni)==2:
        s =  0.25*(dni[0]+dni[1])**2
        tot2 += s
        sum_count2 += 1

        tot_sum += s
        sum_count += 1

sys.stderr.write('# dn2: all   single chain   double chain \n')
print dt, " ", tot_sum/sum_count, " ", tot1/sum_count1, " ", tot2/sum_count2 
