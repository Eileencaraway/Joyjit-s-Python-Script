#!/usr/bin/env python

import sys
import os
import StringIO
import math
import numpy
from numpy import *
from histogram import *

#####################################################################################
#####################################################################################
"""
The script computes ratio of free ions and single paired ions from "Li-TFSIindex.dat"
and "MPPY-TFSIindex.dat" 
"""
#####################################################################################
#####################################################################################

if(len(sys.argv)<6) :
    sys.stderr.write('Usage : -input diffusion-file1 diffusion-file2 ratio tmin tmax ')
    print 
    exit()

carg =1
tot_peo=0
nm_peo=0
tot_li=0
tot_mppy=0
tot_tfsi=0
for word in sys.argv[1:]:
    if word[0] == "-":

        if word == "-input":
            carg += 1
            ifile = open(sys.argv[carg])
            param = ifile.readlines()
            tot_peo  = int(param[0])
            nm_peo   = int(param[1])
            tot_li   = int(param[2])
            tot_mppy = int(param[3])
            tot_tfsi = int(param[4])
            carg +=1

tot_ion = tot_li+tot_tfsi+tot_mppy
dfile1 = sys.argv[carg]
carg +=1
dfile2 = sys.argv[carg]
carg +=1
rfile = sys.argv[carg]
carg +=1
tmin = float(sys.argv[carg])
carg +=1
tmax = float(sys.argv[carg])
carg +=1

def extractData(data, alist) :
    for j in range(0, len(data)):
        
        if not (data[j].startswith("#") or data[j].startswith("\n")) :
            tmp = fromstring(data[j],sep=" ")
            alist.append(tmp)
    
    sys.stderr.write('# nb. of lines '+str(len(alist))+'\n') 
    return 0


#################################################################################
""" reading data files  """
#################################################################################
f1    = open(dfile1)
data1 = f1.readlines()
f1.close()
list1 = []
extractData(data1, list1)

if (tot_mppy>0) :
    os.system("math_calcformula.py '("+str(tot_li)+"*y1+"+str(tot_tfsi)+"*y4+"+str(tot_mppy)+"*y5)/"+str(tot_ion)+"' "+dfile1+" > avg.dif")
else :
    os.system("math_calcformula.py '("+str(tot_li)+"*y1+"+str(tot_tfsi)+"*y4)/"+str(tot_ion)+"' "+dfile1+" > avg.dif")

f2    = open("avg.dif")
data2 = f2.readlines()
f2.close()
list2 = []
extractData(data2, list2)

f3    = open(dfile2)
data3 = f3.readlines()
f3.close()
list3 = []
extractData(data3, list3)

f4    = open(rfile)
data4 = f4.readlines()
f4.close()
list4 = []
extractData(data4, list4)


print "# time      collective-MSD    avg/collective"
for j in range(0, len(list4)):
    
    if not list4[j][0] == list1[j][0]:
        print '# time mismatch'
        exit()

    if not list4[j][0] == list3[j][0]:
        print '# time mismatch'
        exit()

    if (tot_mppy>0) :
        y = tot_li*list4[j][1]*list3[j][1] + tot_tfsi*list4[j][1]*list3[j][2] + tot_mppy*list1[j][5]
        y = y/tot_ion

    else :
        y = tot_li*list4[j][1]*list3[j][1] + tot_tfsi*list4[j][3]*list3[j][2]
        y = y/tot_ion

    print list4[j][0], y, list2[j][1]/y
