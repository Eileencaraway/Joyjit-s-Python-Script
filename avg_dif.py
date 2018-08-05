#!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *

L = sys.argv
first = 0
#values = 0
sq_values = 0
sum_column = 0


for filename in sys.argv[1:]:
    f = open(filename)
    data = f.readlines()
    List = []

    for j in range(0, len(data)):
        if not data[j].split()[0] == '#':
            tmp = fromstring(data[j],sep=" ")
            List.append(tmp)

    if first == 0:
       Sum_List = List
       first = 1
       
    else:
        for i in range(0, len(List)):
            Sum_List[i] += List[i]
    
    sys.stderr.write('import '+filename+' size-'+str(len(List))+'\n')
    f.close()

length = len(Sum_List)
No_files = len(L)-1
#print No_files, length
val = 0
sum_values = zeros([len(Sum_List[0])], 'f');
#sq_values = zeros([len(Sum_List[0])], 'f');

for i in range(0, length):
    values = []
    for j in range(0, len(Sum_List[i])):
        if j == 0:
            val = Sum_List[i][j]/No_files
            values.append(val)
            print val,
        else:
            val = Sum_List[i][j]/Sum_List[i][0]#divides all column by column_zero of each line
            values.append(val)
            print val,

        if j == len(Sum_List[i])-1:
            sum_values += values
            #sum_values += values*values

    print
    #values = Sum_List[i]
    #sq_values += values*values

#print sum_values, sq_values

result = zeros([1, 2*len(tmp)], 'f'); 
for i in range(0, len(tmp)):
    average = sum_values[i]/length
    #variance = sq_values[i]/(No_files*No_files*length) - average*average
    #stddev = math.sqrt(variance)
    result[0][2*i] = average
    #result[0][2*i+1] = variance

print "#Meanvalues and #variance = ", 
for j in range(0, len(result[0])):
    print result[0][j],
    
    

