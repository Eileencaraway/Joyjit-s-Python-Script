#! /usr/bin/python
import sys
from numpy import *
from polarstat import *
from atoms import *

if len(sys.argv)<11:
    print "Usage: fluidAnalyser.py xmin ymin xmax ymax nx ny rmax nr infile"

xmin = float(sys.argv[1])
ymin = float(sys.argv[2])
xmax = float(sys.argv[3])
ymax = float(sys.argv[4])
nx = int(sys.argv[5])
ny = int(sys.argv[6])
rmax = float(sys.argv[7])
nr = int(sys.argv[8])

f = FluidAnalyser(xmin,ymin,xmax,ymax,nx,ny,rmax,nr)
f.initialize()

for filename in sys.argv[9:]:
    print "Reading", filename
    datafile = file(filename,'rb')
    [cell, all, format] = readFile(datafile)
    datafile.close()
    
    listnb = size(all)
    print "Found ", listnb, " list(s)"

    X = []
    Y = []
    R = []
    for list in all:
	    N = size(list.data)
	    for i in range(0, N):
		    X.append(float(list.data[i][0]))
		    Y.append(float(list.data[i][1]))
		    R.append(float(list.radius))

    f.instanciate(X,Y,R,X,Y)

f.finalize()

outfile = open('g','w')
for i in range(0,len(f.g)):
	outfile.write(str(f.rValue(i+0.5))+" "+str(f.g[i])+"\n")

outfile.close()
