#!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *

if size(sys.argv)<2:
    sys.stderr.write("Usage: filename")
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

first = 0
sum_fileData = []
for filename in sys.argv[carg:]:
    f = open(filename)
    data = f.readlines()
    f.close()
    List = []

    for j in range(0, len(data)):
        if not data[j].split()[0][0] == '#':
                tmp = fromstring(data[j],sep=" ")
                if (tmp[0]>=lower_lt and tmp[0]<=upper_lt):      #for shear+thermal
                #if (tmp[0]>=1000.00 and tmp[0]<=6000.00): # for thermal 
                    List.append(tmp)

    if first == 0:
        Sum_List = zeros((len(List),len(List[0])))
        No_rows = len(List)
        No_columns = len(List[0])
        No_files = 1
        Sum_Line = 0
        for i in range(0, len(List)):
            for j in range(0, len(List[0])):
                if j == 0:
                    Sum_List[i][j] = List[i][j]

                else : 
                    l = List[i][j]/List[i][0]
                    Sum_List[i][j] = l
                    List[i][j] = l

            Sum_Line += List[i]
        sum_fileData.append(Sum_Line)
        first = 1

    else:
        if len(List)== No_rows:
            No_files +=1
            Sum_Line = 0
            for i in range(0, len(List)):
                for j in range(0,len(List[0])):
                    if j==0 :
                        Sum_List[i][j] += List[i][j]
                    else :
                        l = List[i][j]/List[i][0]
                        Sum_List[i][j] += l
                        List[i][j] = l
                Sum_Line += List[i]
            sum_fileData.append(Sum_Line)
                         
                    
    sys.stderr.write('import '+filename+' size-'+str(len(List))+'\n')

sys.stderr.write('No_files = '+str(No_files)+'\n')

for i in range(0, No_rows):
    for j in range(0, No_columns):
        print Sum_List[i][j]/No_files,
    print
    

sum_files = 0
sum_sqfiles = 0
for f in range(0, No_files):
    values = sum_fileData[f]
    sum_files += values
    sum_sqfiles += values*values
    
sum_files = sum_files/No_rows
sum_sqfiles = sum_sqfiles/No_rows/No_rows
result = zeros([1, 2*No_columns], float); 

for i in range(0, No_columns):
    average = sum_files[i]/No_files
    if No_files == 1:
        variance = 0
    else:
        variance = (sum_sqfiles[i]-No_files*average*average)/(No_files-1) #Bessel correction
        if variance < 0:  #floating point error
            variance = -1.0*variance
    stdErr = 1.3*math.sqrt(variance/No_files) #student's t-distribution
    result[0][2*i] = average
    result[0][2*i+1] = stdErr

print "#Meanvalues and #variance = ", 
for j in range(0, len(result[0])):
    print result[0][j],


