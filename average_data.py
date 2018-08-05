#! /usr/bin/env python

# given a datafile with energy, pressure, stress,... data, perform averages
import sys
import os
import StringIO
import math
import numpy
from numpy import *
from data import *

if len(sys.argv) < 2:
    sys.stderr.write('Usage : '+sys.argv[0]+' filelist')
    sys.exit(0)

stat = DataCollector(0.2,100)

for filename in sys.argv[1:]:

    sys.stderr.write('import '+filename+' ')
    [data, header] = readData(filename)
    sys.stderr.write(str(len(data))+'\n')

    stat.collect(data)

stat.finalize()

for line in header:
    print line,

[N,M] = shape(stat.M)
for i in range(0, N):
    for j in range(0, M):
        print stat.M[i][j],
    print

Ndatalines = size(stat.M,0)
Ninst = len(stat.means)
m = mean(stat.means,0)
v = mean(stat.means*stat.means,0)-m*m
m2 = mean(stat.mean2s,0)
v2 = mean(stat.mean2s*stat.mean2s,0)-m2*m2

print "# mean values (",stat.Ninst,"files, ",Ndatalines,"lines) = ",

for i in range(1,len(m)):
    print m[i],1.3*sqrt((v[i])/(Ninst-1)),
print
    
print "# mean vars (",stat.Ninst,"files, ",Ndatalines,"lines) = ",
for i in range(1,len(m2)):
    print m2[i],1.3*sqrt((v2[i])/(Ninst-1)),
print


