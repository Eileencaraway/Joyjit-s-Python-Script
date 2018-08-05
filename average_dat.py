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
    print filename
    f = open(filename)
    data = f.readlines()
    count = 0

    for j in range(0, len(data)):
        if data[j].split()[0] == '#':
            count += 1
        else:
            if first == 0:
                tmp = fromstring(data[j],sep=" ")
                first = 1
         
    mat = zeros([len(data),len(tmp)], 'f')
    for j in range(count, len(data)):
        mat[j] = fromstring(data[j],sep=" ")
    if first == 1:
        matrix = mat
        first = 2
    else:
        matrix += mat

    f.close()

#print matrix

No_files = len(L)-1
length = len(data)-count
print No_files, length

for i in range(count, len(data)):
    sum_column += matrix[i]
    values = matrix[i]
    sq_values += values*values
#print sum_column, sq_values

for i in range(0, len(tmp)):
    average = sum_column[i]/(No_files*length)
    stddev = math.sqrt(sq_values[i]/(No_files*No_files*length) - average*average)
    print average, stddev
    


