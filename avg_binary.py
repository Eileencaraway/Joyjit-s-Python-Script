#!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *

first        = 0
No_files     = 0
sum_fileData = []


for filename in sys.argv[1:]:

    f           = open(filename, 'rb')
    no_column   = fromfile(f,'int32',1)
    data        = fromfile(f,'float32')
    factor      = size(data)/no_column
    newdatasize = factor*no_column
    newdata     = [data[i] for i in range(0,newdatasize)]
    reform_data = numpy.reshape(newdata, (-1,no_column))

    # print '# data factor newdatasize = ', size(data), ' ', factor, ' ', newdatasize, ' ', size(newdata)   

    if first == 0:
        Sum_List   = reform_data
        No_rows    = len(Sum_List)
        No_columns = len(Sum_List[0])
        No_files   = 1
        Sum_Line   = 0

        for i in range(0,  No_rows):
            Sum_Line += reform_data[i]

        sum_fileData.append(Sum_Line)
        first = 1
            
    else:
        if len(reform_data)== No_rows:
            No_files +=1
            Sum_List += reform_data
            Sum_Line  = 0

            for i in range(0,  No_rows):
                Sum_Line += reform_data[i]

            sum_fileData.append(Sum_Line)
                    
    
    sys.stderr.write('import '+filename+' size-'+str(len(reform_data))+'\n')
    f.close()

sys.stderr.write('No_files = '+str(No_files)+'\n')

for i in range(0, No_rows):
    for j in range(0, No_columns):
        print Sum_List[i][j]/No_files,
    print
        
sum_files   = 0
sum_sqfiles = 0

for f in range(0, No_files):
    values       = sum_fileData[f]
    sum_files   += values
    sum_sqfiles += values*values
        


sum_files   = sum_files/No_rows
sum_sqfiles = sum_sqfiles/No_rows/No_rows
result      = zeros([1, 2*No_columns], float); 

for i in range(0, No_columns):
    average = sum_files[i]/No_files

    if No_files == 1:
        variance = 0
    else :
        variance = (sum_sqfiles[i]-No_files*average*average)/(No_files-1) #Bessel correction

        if variance < 0:  #floating point error
            variance = -1.0*variance

    stdErr           = 1.3*math.sqrt(variance/No_files) #student's t-distribution
    result[0][2*i]   = average
    result[0][2*i+1] = stdErr
        
print "#Results no_files = ", No_files," ",   
for j in range(0, len(result[0])):
    print result[0][j],
                
 
 
