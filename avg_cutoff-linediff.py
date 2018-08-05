#!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *

L = sys.argv
first = 0
values = 0
sq_values = 0
sum_column = 0


for filename in sys.argv[1:]:
    f = open(filename)
    data = f.readlines()
    List = []

    for j in range(0, len(data)):
        if not data[j].split()[0] == '#':
            tmp = fromstring(data[j],sep=" ")
            if (tmp[0]>=3.00 and tmp[0]<=4.00):
                List.append(tmp)

    if first == 0:
       Sum_List = List
       l = array(List)
       Sqsum_List = l*l
       length = len(Sum_List)
       No_files = 1
       first = 1
       
    else:
        if len(List)== length:
            No_files += 1
            l = array(List)
            Sum_List += l
            Sqsum_List += l*l
                
    sys.stderr.write('import '+filename+' size-'+str(len(List))+'\n')
    f.close()

sys.stderr.write('No_files = '+str(No_files)+'\n')
sl = array(Sum_List)
Sumsq_List = sl*sl
computeError = (No_files*Sqsum_List - Sumsq_List)/No_files/No_files

val = 0
Sum_values = zeros([len(Sum_List[0])], 'f');
Sqsum_values = zeros([len(Sum_List[0])], 'f');

for i in range(0, length):
    for j in range(0, len(Sum_List[i])):
        if computeError[i][j]<0:
            computeError[i][j]= -1.0*computeError[i][j]
            #print i,j
        if j == 0:
            val = Sum_List[i][j]/No_files
            Sum_values[j] += val
            Sqsum_values[j] += val*val
            print val, math.sqrt(computeError[i][j]),

        else:
            val = Sum_List[i][j]/Sum_List[i][0]#divides all column by column_zero of each line
            Sum_values[j] += val
            Sqsum_values[j] += val*val
            print val, math.sqrt(computeError[i][j]),

    print
    
result = zeros([1, 2*len(tmp)], 'f'); 
for i in range(0, len(tmp)):
    average = Sum_values[i]/length
    variance = Sqsum_values[i]/length - average*average
    if variance<0:
        variance = -1.0*variance
    stddev = math.sqrt(variance)
    result[0][2*i] = average
    result[0][2*i+1] = stddev

print "#Meanvalues and #variance = ", 
for j in range(0, len(result[0])):
    print result[0][j],
    

