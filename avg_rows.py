#!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *

first        = 0
No_files     = 0
No_rows      = 0
sum_fileData = []

def notStr(List):
    num=True
    try:
        float(List[0])
    except ValueError:
        num=False
    if num:
        return True
    else:
        try:
            float(List[1])
        except ValueError:
            num=False
    
    return num

for filename in sys.argv[1:]:
    if not os.path.exists(filename):
        continue
        
    f = open(filename)
    data = f.readlines()
    f.close()
    List = []

    for j in range(0, len(data)):
        if not (data[j].startswith("#") or data[j].startswith("\n") or data[j].startswith('ERROR')) :
        #if notStr(data[j]):
            tmp = fromstring(data[j],sep=" ")
            List.append(tmp)

    rows = len(List)
    if rows < 1:
        continue

    if first == 0:
        No_files   = 1
        Sum_List   = list(List)
        No_rows    = len(Sum_List)
        No_columns = len(Sum_List[0])
        first      = 1   
    else:
        No_files  += 1
        minval     = min(No_rows, rows)
        #sys.stderr.write('#'+str(rows)+' '+str(No_rows)+'\n')
        for r in range(minval):
            for c in range(No_columns):
                Sum_List[r][c] += List[r][c] 
                
        if rows < No_rows:
            for r in range(rows, No_rows):
                Sum_List[r][0] += Sum_List[r][0]/(No_files-1.0)

        if rows > No_rows:
            for r in range(No_rows, rows):
                Sum_List.append([0 for c in range(No_columns)])
                for c in range(No_columns):
                    if c==0:
                        Sum_List[r][c] += No_files*List[r][c] 
                    else:
                        Sum_List[r][c] += List[r][c] 
                    
            No_rows=rows

   
    sys.stderr.write('#import '+filename+' size-'+str(len(List))+'\n')

sys.stderr.write('#No_files = '+str(No_files)+'\n')
for i in range(0, No_rows):
    for j in range(0, No_columns):
        print Sum_List[i][j]/No_files,
    print
    
"""
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

 """   

