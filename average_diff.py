#! /usr/bin/env python

# given a datafile with energy, pressure, stress,... data, perform averages
import sys
import os
import StringIO
import math
import numpy
from numpy import *

def readlines(filename):
    file = open(filename)
    sys.stderr.write('import '+filename)
    data = file.readlines()
    file.close()
    return data

if len(sys.argv) < 2:
    sys.exit(0)

if not os.path.exists(sys.argv[1]):
    sys.exit(0)

xmin = 1.5
xmax = 2.5

data0 =  readlines(sys.argv[1])
Nlines = len(data0)
sys.stderr.write(' '+str(Nlines)+'\n')

linetype = empty(Nlines, bool)
vals = []
vals2 = []

Ndatalines = 0
meanvals = []
meanvalues = empty(0)

for i in range(0, Nlines):
    words = data0[i].split()

    if words[0][0]=="#" or words[0]=="&":
        linetype[i] = False
        vals.append(empty(0))
        vals2.append(empty(0))
        print data0[i],
    else:
        linetype[i] = True
        values = fromstring(data0[i],sep=" ")
        values[1:] /= values[0]
	vals.append(values)
        vals2.append(values*values)

        if values[0] >= xmin and values[0] <= xmax:
            if Ndatalines == 0:
                meanvalues = zeros(len(values))

            meanvalues += values
            Ndatalines += 1

meanvalues /= Ndatalines
meanvals.append(meanvalues)

Nfiles = 1

for filename in sys.argv[2:]:
    data = readlines(filename)
    sys.stderr.write(' '+str(len(data)))

    if len(data) != Nlines:
        sys.stderr.write(' size mismatch')
        
    if len(data)>=Nlines:
        Ndatalines = 0
        for i in range(0, Nlines):
            if linetype[i]:
                if data[i][0] != data0[i][0]:
                    sys.stderr.write(' file mismatch '+str(data0[i][0])+' '+sys.argv[1]+' '+filename+'\n')
                values = fromstring(data[i],sep=" ")
		values[1:] /= values[0]
                vals[i] += values
		vals2[i] += values*values
                if values[0] >= xmin and values[0] <= xmax:
                    if Ndatalines == 0:
                        meanvalues = zeros(len(values))

                    meanvalues += values
                    Ndatalines += 1

        meanvalues /= Ndatalines
        meanvals.append(meanvalues)
        Nfiles += 1

    sys.stderr.write('\n')

    
for i in range(0, Nlines):
    if linetype[i]:
        vals[i] /= Nfiles
	vals2[i] /= Nfiles

        print vals[i][0],
        for j in range(1,len(vals[i])):
            print vals[i][j], 1.3*sqrt((vals2[i][j]-vals[i][j]*vals[i][j])/(Nfiles-1)),
        print

meanmean = meanvals[0]
mean2mean = meanvals[0] * meanvals[0]

for i in range(1,len(meanvals)):
    meanmean += meanvals[i]
    mean2mean += meanvals[i] * meanvals[i]

meanmean /= len(meanvals)
mean2mean /= len(meanvals)

Ninst = Nfiles
if Ninst == 1:
    Ninst = 2

print "# mean values (",Nfiles,"files, ",Ndatalines,"lines) = ",

for i in range(1,len(meanmean)):
    print meanmean[i],1.3*sqrt((mean2mean[i]-meanmean[i]*meanmean[i])/(Ninst-1)),
print
    
    


