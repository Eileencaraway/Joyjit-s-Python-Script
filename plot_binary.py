#!/usr/bin/env python

import sys
import os
from math import *
import numpy
from numpy import *
from pylab import *
import matplotlib.pyplot

for filename in sys.argv[1:]:

    f           = open(filename, 'rb')
    no_columns   = fromfile(f,'int32',1)
    data        = fromfile(f,'float32')
    factor      = size(data)/no_columns
    newdatasize = factor*no_columns
    newdata     = [data[i] for i in range(0,newdatasize)]
    #reform_data = numpy.reshape(newdata, (-1,no_columns))
    #no_rows    = len(reform_data)
    r_data = numpy.reshape(newdata, (-1,no_columns))
    no_rows    = len(r_data)
    f.close()

    sys.stderr.write('reading file: '+str(filename)+' found '+str(no_rows)+' no. of rows \n')

reform_data=[]
for i in range(0, no_rows):
    if i%2.0 == 0 :
        reform_data.append(r_data[i])

#for i in range(0, no_rows):
#    for j in range(0, no_columns):
#        print reform_data[i][j],
#    print
      
no_rows = len(reform_data)
print no_rows 
x=[]
y=[]
for i in range(0, no_rows):
    x.append(reform_data[i][0])
    y.append(reform_data[i][3])

fig = figure()
for i in range(0, no_rows):
    px=reform_data[i][0]
    py=reform_data[i][3]

    plot(x, y, 'k', linewidth=0.25)
    l = plot([px], [py], 'bo')
    axis([reform_data[0][0]-0.0001, reform_data[no_rows-1][0]+0.0001, min(y)-0.001, max(y)+0.001])
    setp(l, 'markersize', 3.5)
    #setp(l, 'markerfacecolor', 'b')

    xlabel('strain', x=0.9)
    ylabel('stress',rotation='vertical', y=0.82)
    name = filename+'-'+str(i).zfill(3)+'.png'
    savefig(name)
    fig.clf()
  
#xticks(fontsize='xx-large', fontstyle='italic')
#yticks(fontsize='xx-large', fontstyle='italic')
#show()

 
