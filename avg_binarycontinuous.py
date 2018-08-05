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
finalpoint = 0
carg =1 
L = size(sys.argv)
if(L<4) :
    sys.stderr.write('Usage : No_system ' ' T' ' gdot ')
    print 
    exit()

for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-18":
            finalpoint = 1
            carg      += 1
       
smax  = int(sys.argv[carg])
carg +=1
T     = sys.argv[carg]
carg +=1
gdot  = sys.argv[carg]

if finalpoint == 1:
    gammalist = [ 4, 8, 13, 18 ]
else:
    gammalist = [ 2, 4, 8, 13 ]
    
    
for s in range(0, smax):
    all_data = numpy.zeros((0,8)) # initialize all_data file 
    true     = 1

    for gamma in gammalist :
        filename = 'sys-'+str(s).zfill(3)+'/shear-T-'+str(T)+'-gdot-'+str(gdot)+'-g-'+str(gamma)+'.bin'
        
        if os.path.exists(filename):
            # sys.stderr.write(filename+'\n')
            f            = open(filename, 'rb')
            no_column    = fromfile(f,'int32',1)

            if true == 1:
                all_data = numpy.zeros((0,no_column))
                true     = 0

            data         = fromfile(f,'float32')
            factor       = size(data)/no_column
            newdatasize  = factor*no_column
            newdata      = [data[i] for i in range(0,newdatasize)]
            reform_data  = numpy.reshape(newdata, (-1,no_column))
            all_data     = concatenate([all_data, reform_data],0)
            f.close()
            
    if size(all_data) != 0:
        if first == 1:
            Sum_data   = all_data
            No_rows    = len(all_data)
            No_columns = no_column
            No_files   = 1
            Sum_Line   = 0
            
            for i in range(0,No_rows):
                Sum_Line += all_data[i]
                
            sum_fileData.append(Sum_Line)
            first = 0
            
        else:        
            if len(all_data) == No_rows:
                Sum_data += all_data
                No_files +=1
                Sum_Line  = 0
                
                for i in range(0,No_rows):
                    Sum_Line += all_data[i]
                
                sum_fileData.append(Sum_Line)
        
                    
    
    sys.stderr.write('import '+filename+' shape-'+str(shape(all_data))+'\n')
    

sys.stderr.write('No_files = '+str(No_files)+'\n')
#for i in range(0, len(Sum_data)):
#   for j in range(0, No_columns):
#     print Sum_data[i][j]/No_files,
# print 

#stress = [ Sum_data[i][4] for i in range(0,len(Sum_data)) ]
#fftdata = fft(stress)

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
    else:
        variance = (sum_sqfiles[i]-No_files*average*average)/(No_files-1) #Bessel correction
        if variance < 0:  #floating point error
            variance = -1.0*variance

    stdErr           = 1.3*math.sqrt(variance/No_files) #student's t-distribution
    result[0][2*i]   = average
    result[0][2*i+1] = stdErr
        

if finalpoint == 1:
    file = open('shear_avg-T-'+str(T)+'-gdot-'+str(gdot)+'-g-18.bin', 'w')
else:
    file = open('shear_avg-T-'+str(T)+'-gdot-'+str(gdot)+'-g-13.bin', 'w')

print "#Meanvalues and #variance = ",
print >> file, "#Meanvalues and #variance = ",
for j in range(0, len(result[0])):
    print result[0][j],
    print >> file, result[0][j],
               
#file = open("strainfft", 'w')
#for j in range(0, 100):
#    print >> file, j, abs(fftdata[j])
    
