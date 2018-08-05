#!/usr/bin/env python

import sys
import os
import StringIO
import math
import numpy
from numpy import *

L = size(sys.argv)
if(L<2) :
    sys.stderr.write('Usage : i. total number, ii. dimension of a cube')
    print 
    exit()

pdb = 1
carg =1
tot_nb = int(sys.argv[carg])
carg +=1
side   = float(sys.argv[carg])
carg +=1

print "# generating ", tot_nb," numbers inside a cubic box of dimension ", side

for i in range(tot_nb):
    if pdb==1 :
        print "ATOM  ", str(8400+i).rjust(4), "Li1".rjust(4), "LI".rjust(1), "", str(742+i).rjust(5), "", str("%.3f" %(random.random()*side)).rjust(10), str("%.3f" %(random.random()*side)).rjust(7), str("%.3f" %(random.random()*side)).rjust(7)

    else :
        print random.random()*side, " ", random.random()*side, " ", random.random()*side
    
