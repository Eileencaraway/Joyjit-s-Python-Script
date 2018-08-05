#!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *

#######################################################################################
# print maximum, minimum and average values of a column 
#######################################################################################

No_rows = 0
verbose = False
carg    = 1
L = size(sys.argv)

if(L<2) :
    sys.stderr.write('Usage : column id (starts with 1),  filenames')
    print 
    exit()

for word in sys.argv[carg:]:
    if word[0] == "-":
        if word == "-v":
            verbose = True
            carg += 1

cid   = int(sys.argv[carg])-1
carg += 1
for filename in sys.argv[carg:]:
    if not os.path.exists(filename):
        continue
        
    f = open(filename)
    data = f.readlines()
    f.close()

    List = []
    mini = 0
    maxi = 0
    aveg = 0
    minr = 0
    maxr = 0
    rows = 0
    First=True

    for j in range(0, len(data)):
        if not (data[j].startswith("#") or data[j].startswith("\n") or data[j].startswith('ERROR')) :
            tmp = fromstring(data[j],sep=" ")
            List.append(tmp)

            if tmp[cid] > maxi or First:
                maxi = tmp[cid]
                maxr = rows
                
            if tmp[cid] < mini or First:
                mini = tmp[cid] 
                minr = rows

            First=False
            aveg += tmp[cid]
            rows += 1

    sys.stderr.write('#####################################################################\n')
    sys.stderr.write('# reading column : '+str(cid+1)+' of '+filename+'\n')
    sys.stderr.write('# maximum minimum average \n')
    sys.stderr.write('  '+str(maxi)+' '+str(mini)+' '+str(aveg/rows)+'\n')
    sys.stderr.write('# row with maximum value \n')
    str0=' '
    for c in range(len(List[maxr])):
        str0+=' %.5e'%List[maxr][c]
    sys.stderr.write(str0+' \n')
    sys.stderr.write('# row with minimum value \n')
    str1=' '
    for c in range(len(List[minr])):
        str1+=' %.5e'%List[minr][c]
    sys.stderr.write(str1+' \n')
    sys.stderr.write('#####################################################################\n')

    #print List[minr][3], " ", List[minr][0]
