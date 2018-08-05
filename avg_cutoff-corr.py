#!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *

if size(sys.argv)<3:
    sys.stderr.write("Usage: time filename")
    print
    exit()

carg = 1
lower_lt = 4.00
upper_lt = 8.00
for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-set":
            carg += 1
            lower_lt = float(sys.argv[carg])
            carg += 1
            upper_lt = float(sys.argv[carg])
            carg += 1

dt = sys.argv[carg]
carg += 1

for filename in sys.argv[carg:]:
    f = open(filename)
    data = f.readlines()
    f.close()
    List = []

    for j in range(0, len(data)):
        if not data[j].split()[0][0] == '#':
                tmp = fromstring(data[j],sep=" ")
                if (tmp[0]>=lower_lt and tmp[0]<=upper_lt):      
                    List.append(tmp)


    No_rows = len(List)
    No_columns = len(List[0])
    Sum_Line = 0
    for i in range(0, len(List)):
        for j in range(0, len(List[0])):
            if j > 1:
                l = List[i][j]*List[i][1]
                List[i][j] = l

        Sum_Line += List[i]

    sys.stderr.write('import '+filename+' size-'+str(len(List))+'\n')


#for i in range(0, No_rows):
#    for j in range(0, No_columns):
#        print List[i][j],
#    print
    
print dt, " ",
for i in range(0, No_columns):
    if i < 2:
        print Sum_Line[i], " ",
    else:
        print Sum_Line[i]/Sum_Line[1], " ",

print 
