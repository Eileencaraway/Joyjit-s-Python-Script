#! /usr/bin/env python

import sys
import os
import numpy
from numpy import *
from math import *

if size(sys.argv)<2:
    sys.stderr.write("Usage: ifilename")
    print
    exit()

carg = 1
 
def readAndWriteFile(readfile, wfile):
    rf = open(readfile)
    data = rf.readlines()
    rf.close()
    wf = open(wfile, 'w')
            
    print len(data)
    nb_peo = 0
    for i in range(0, len(data)):
        tmp = data[i].split()
        
        if len(tmp) == 6:
            sdigits = ''.join([l for l in tmp[0] if l.isdigit()])
            ndigits = ''.join([l for l in tmp[0] if not l.isdigit()])
            
            if tmp[1] == 'CT1':
                nb_peo += 1 
                
            if int(sdigits) != nb_peo:
                sdigits = str(nb_peo)

            print >> wf, "ATOM  ", tmp[2].rjust(4), tmp[1].rjust(4), ndigits.rjust(4), "", sdigits.rjust(4), "", tmp[3].rjust(9), "", tmp[4].rjust(9), "", tmp[5].rjust(9)  
            
    wf.close()

        
wfilename  = 'pdb'
readfile = sys.argv[carg]
if os.path.exists(readfile):
    readAndWriteFile(readfile, wfilename)
else:
    print readfile, " does not exist."
                


