#!/usr/bin/env python

import sys
import os
import StringIO
from pylab import *
from math import pi, atan2, sin, cos, sqrt, floor, exp
from matplotlib.patches import Ellipse
from atoms import *

shift = [float(sys.argv[1]), float(sys.argv[2])]
files = []
findex = 0
for filename in sys.argv[3:]:

    fname = filename+".png"

    if not os.path.isfile(fname):
	print "Reading", filename

	datafile = file(filename,'rb')
    	[cell, all, format] = readFile(datafile)
	
    	if format&OUTPUT_ARRAY != 0:
		print "Found array"
		mean2 = []
		maxm2 = []
		for list in all:
        		N = size(list.data)
			print N
			a = fromfile(datafile, float, 2*N)
			a.resize(N,2)
			m2 =  [a[i][0]+a[i][1] for i in range(0, N)]
			mean2.append(m2)
			maxm2.append(max(m2))
	
		norm = max(maxm2)
        	norm = 0.02
		for i in range(0, len(mean2)):
 #            mean2[i] /= norm
            		for j in range(0, len(mean2[i])):
				mean2[i][j] = mean2[i][j]/norm
                		if mean2[i][j] > 1:
                    			mean2[i][j] = 1
		
		print max(mean2[0]), max(mean2[1]), max(maxm2)

    	datafile.close()
    
    	listnb = size(all)
    	print "Found ", listnb, " list(s)"

    	fig = figure(figsize=(8,8))
    	ax = fig.add_subplot(111, aspect='equal')

    	listindex = 0
    	for list in all:
        	N = size(list.data)
        	print N, list.radius

# if format < 2:
# else:
        	X =  [float(list.data[i][0]+shift[0]) for i in range(0, N)]
        	Y =  [float(list.data[i][1]+shift[1]) for i in range(0, N)]
        	R =  [float(list.radius) for i in range(0, N)]
        	cell.projectIntoBaseCell(X,Y)

        
        	if format & OUTPUT_VELOCITIES:
            		U =  [list.data[i][2] for i in range(0, N)]
            		V =  [list.data[i][3] for i in range(0, N)]

            	print min(U), max(U), min(V), max(V)

            	quiver(X,Y,U,V)

		if format & OUTPUT_ENERGIES:
            		E =  [-list.data[i][4] for i in range(0, N)]
            		m = min(E)
            		M = max(E)
            		print "Min E = ", m, M

            		for i in range(0, len(E)):
                		E[i] = (E[i]+2)/5
                		if E[i] > 1:
                    			E[i] = 1
                		else:
                    			if E[i] < 0:
                        			E[i] = 0

            		drawAtoms(ax, X, Y, R) 
            		colorAtoms(ax, X, Y, R, E)
            
#        else:
#            if format&OUTPUT_ARRAY != 0:
#		drawAtoms(ax, X, Y, R)
#		colorAtoms(ax, X, Y, R, mean2[listindex])
        #		colorAtoms(ax, X, Y, mean2[listindex], [1 for i in range(0, N)])
#            else:
#		drawAtoms(ax, X, Y, R)
 
        	if format & OUTPUT_FORCES:
            		FX =  [float(list.data[i][4]) for i in range(0, N)]
            		FY =  [float(list.data[i][5]) for i in range(0, N)]

            		print min(FX), max(FX), min(FY), max(FY)

            		quiver(X,Y,FX,FY, color='r')

        	margin = 8
        	ax.set_xlim(-margin, cell.L[0]+margin)
        	ax.set_ylim(-margin, cell.L[1]+margin)
	listindex += 1

    	print 'Saving frame', fname
    	savefig(fname)
    	files.append(fname)
    	findex = findex+1


print 'Making movie animation.mpg - this may take a while'
os.system("mencoder 'mf://_tmp*.png' -mf type=png:fps=5 \
  -ovc lavc -lavcopts vcodec=wmv2 -oac copy -o animation.mpg")


# mencoder 'mf://*.png' -mf type=png:fps=20 -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=2160000 -nosound -oac copy -o animation.avi
