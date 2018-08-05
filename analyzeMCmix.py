#! /usr/bin/env python

import sys
import os
import numpy
from numpy import *
from math import *

subsystem = -1
Gibbs = False
dsteps = 0
Old = False

ar = ['TEMP', 'PRESS', 'NMOL', 'NCH4', 'NCF4', 'MASS', 'VOL', 'MDENSITY', 'NDENSITY', 'EPOT']
#ar = ['TEMP', 'PRESS', 'NMol', 'VOL', 'Density', 'EPOT']
   
def readFile(readfile):
    rf = open(readfile)
    data = rf.readlines()
    rf.close()
    
    periods=11
    time_steps = 0
    param_avg  = 0
    param_sqavg = 0
    i=0
    ts=0
    while (i <len(data)):
        tmp = data[i].split()
        
        if (len(tmp) > 0 and tmp[0] == 'NSTEP'):

            if(Gibbs):
                periods = 9 
                pre_line = data[i-1].split()

                if int(pre_line[2]) == subsystem :
                    if(ts==0 or ts!= tmp[2]):
                        print tmp[2], " ", # reading number of steps
                        j=i
                        while(j<i+periods) :
                            line = data[j].split()
                            for k in range(len(line)):
                                if(line[k] == name) :
                                    print line[k+2] 
                                    if(int(tmp[2])>dsteps):
                                        val = float(line[k+2])
                                        param_avg += val
                                        param_sqavg += val*val
                                        time_steps += 1
                            
                            j +=1
                
                        i=j
                        ts=tmp[2]
                        

            else :
                if(ts==0 or ts!= tmp[2]):
                    print tmp[2], " ", # reading number of steps
                    j=i
                    while(j<i+periods) :
                        line = data[j].split()
                        for k in range(len(line)):
                            if(line[k] == name) :
                                print line[k+2] # reading the value of the given parameter e.g. EPtot
                                if(int(tmp[2])>dsteps):
                                    val = float(line[k+2])
                                    param_avg += val
                                    param_sqavg += val*val
                                    time_steps += 1
                                 
                        j +=1
                
                    i=j
                    ts=tmp[2]
                
        i += 1

    avg = param_avg/time_steps
    sqavg = param_sqavg/time_steps
    print "# total steps, average, variance, std dev: ", time_steps, avg, (sqavg - avg*avg), sqrt(sqavg - avg*avg)  
######################################################################
######################################################################
carg = 1
if len(sys.argv)<3:
    sys.stderr.write("Usage: (i) ifilename (ii) one of the following numbers \n")
    for i in range(len(ar)): 
        sys.stderr.write(str(i)+" for "+ar[i]+"\n")
        
    print 
    exit()

for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-sub":
            Gibbs = True
            carg += 1
            subsystem = int(sys.argv[carg])
            sys.stderr.write("# reading values for subsystem: "+str(subsystem)+"\n")
            carg += 1
        
        if word == "-d": # delete first n nb. of steps for average
            carg += 1
            dsteps = int(sys.argv[carg])
            sys.stderr.write("# start averaging after time "+str(dsteps)+" \n")
            carg += 1

        
        if word == "-old":
            Old = True
            carg += 1


readfile = sys.argv[carg]
carg +=1
name=ar[int(sys.argv[carg])]
carg +=1

sys.stderr.write("# reading file "+readfile+"\n")
sys.stderr.write("# reading parameter "+name+"\n")

if os.path.exists(readfile):
    readFile(readfile)
else:
    print readfile, " does not exist."


            
                


