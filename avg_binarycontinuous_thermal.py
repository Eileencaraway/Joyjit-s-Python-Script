#!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *
from pylab import *

first = 1
No_rows = 0
No_files = 0
sum_fileData = []

L = size(sys.argv)
if(L<3) :
    sys.stderr.write('Usage : No_system ' ' T' )
    print 
    exit()
    
smax = int(sys.argv[1])
T = sys.argv[2]
timelist = [ 2000, 4000, 8000, 13000 ]


for s in range(0, smax):
    all_data = numpy.zeros((0,8))
    true = 1
    for t in timelist :
        filename = 'sys-'+str(s).zfill(3)+'/thermal-T-'+str(T)+'-t-'+str(t)+'.bin'
        if os.path.exists(filename):
#            sys.stderr.write(filename+'\n')
            f = open(filename, 'rb')
            no_column = fromfile(f,'int32',1)
            if true == 1:
                all_data = numpy.zeros((0,no_column))
                true = 0
            data = fromfile(f,'float32')
            f.close()
            reform_data=numpy.reshape(data, (-1,no_column))
            all_data = concatenate([all_data, reform_data],0)

    if first == 1:
        Sum_data = all_data
        No_rows = len(all_data)
        No_columns = no_column
        No_files = 1
        Sum_Line = 0
        for i in range(0,No_rows):
            Sum_Line += all_data[i]
        sum_fileData.append(Sum_Line)
        first = 0
        
    else:
        if len(all_data) == No_rows:
            Sum_data += all_data
            No_files +=1
            Sum_Line = 0
            for i in range(0,No_rows):
                Sum_Line += all_data[i]
            sum_fileData.append(Sum_Line)
        
                    
    
    sys.stderr.write('import '+filename+' shape-'+str(shape(all_data))+'\n')
    



sys.stderr.write('No_files = '+str(No_files)+'\n')
#for i in range(0, len(Sum_data)):
#    for j in range(0, No_columns):
#        print Sum_data[i][j]/No_files,
#    print 



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
        


file = open('thermal_avg-T-'+str(T)+'-t-13000.bin', 'w') 
print "#Meanvalues and #variance = ",
print >> file, "#Meanvalues and #variance = ",
for j in range(0, len(result[0])):
    print result[0][j],
    print >> file, result[0][j],
               
