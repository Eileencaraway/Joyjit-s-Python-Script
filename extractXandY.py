#! /usr/bin/env python

import sys
import os
import StringIO
from math import *
from numpy import *

#####################################################################################
#####################################################################################
"""
The script:
i. print nth column of the first file and mth column of the second file  
"""
#####################################################################################

################################################################################
"""  reading command pad arguments """
################################################################################
rcolumn  = 0     # reference column
Setlimit = False
drange   = [0.0, 1.0]
Csum     = False # cumulative sum 
xc1      = -1
yc1      = -1
carg     = 1

if len(sys.argv)<5:
    sys.stderr.write("Usage: i. filename ii. column (to be plotted as X started with 1) iii. filename iv. column (to be plotted as Y)")
    print
    sys.exit()
    
for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-v":
            verbose = True
            carg += 1

        if word == "-rc":
            carg += 1
            rcolumn = int(sys.argv[carg])
            print "# reference column ", rcolumn
            carg += 1
        
        if word == "-set":
            Setlimit = True 
            drange = [float(sys.argv[carg+1]), float(sys.argv[carg+2])]
            carg += 3
            print "# range: ", drange
            
        if word == "-csum":
            Csum = True
            carg += 1

        if word == "-com":
            carg += 1
            xc1   = int(sys.argv[carg])-1
            carg += 1
            yc1   = int(sys.argv[carg])-1
            carg += 1


file1 = sys.argv[carg]
carg += 1
x     = int(sys.argv[carg])-1
carg += 1
file2 = sys.argv[carg]
carg += 1
y     = int(sys.argv[carg])-1
carg += 1

################################################################################
"""  reading files and calculate y by the supplied formula """ 
################################################################################
def notStr(List):
    try:
        float(List[0])
        return True
    except ValueError:
        return False
 
def readFile(filename, c, c1):
    f = open(filename)
    data = f.readlines()
    f.close()
    List = []
    
    for j in range(0, len(data)):
        if notStr(data[j]):
            tmp = fromstring(data[j],sep=" ")
            if xc1==-1 and yc1==-1:
                List.append(tmp[c])
            else:
                List.append([tmp[c1], tmp[c]])
            
    sys.stderr.write('# import '+filename+' size-'+str(len(List))+'\n')
    sys.stderr.write('# reading column '+str(c+1)+'\n')
    return List
################################################################################

xcolm = readFile(file1, x, xc1)
ycolm = readFile(file2, y, yc1)

nb_xc = len(xcolm)
nb_yc = len(ycolm)
nb_sc = min(nb_xc, nb_yc)
nb_lc = max(nb_xc, nb_yc)
if xc1==-1 and yc1==-1:
    for c in range(nb_sc):
        print xcolm[c], "        ", ycolm[c]
else:
    c2=0
    for c1 in range(nb_sc):
        while c2 < nb_lc: 
            if nb_sc<nb_xc:
                if abs(ycolm[c1][0]-xcolm[c2][0])==0:
                    break
            else:
                if abs(xcolm[c1][0]-ycolm[c2][0])==0:
                    break
            c2+=1

        if nb_sc<nb_xc:
            print xcolm[c2][1], "        ", ycolm[c1][1], "        ", xcolm[c2][0], "        ", ycolm[c1][0]
        else:
            print xcolm[c1][1], "        ", ycolm[c2][1], "        ", xcolm[c1][0], "        ", ycolm[c2][0]
