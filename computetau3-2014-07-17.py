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
The script computes the residual time td of a Li cation in a polymer chain. 
It reads information from "cation_interchainindex.dat" 

Defination of tau3 = te-ts ; ts: starting time and te = finishing time 
of the file.

At ts store the host peos for a Li+ and then run a loop until the time te where a new
set of host(s) peos is found instead of the old set of host(s).    
If at the end of the loop we do not find a te we will set the last stored time as te.   
"""

#####################################################################################
#####################################################################################

L = size(sys.argv)
if(L<4) :
    sys.stderr.write('Usage : i. -input ii. filename iii. tdis')
    print 
    exit()

No_peos  = 0
No_mms   = 0
No_lis   = 0
No_mppys = 0
No_tfsis = 0
carg =1

for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-input":
            carg += 1
            ifile = sys.argv[carg]
            carg += 1
            fl = open(ifile)
            vals = fl.readlines()
            fl.close()
            if(len(vals)!=5):
                print "!!! Error !!!"
                print "# check the order --> Number of peos, Number of monomers, Lis, MPPYs, TFSIs in ",ifile
                exit()
            No_peos  = int(vals[0])
            No_mms   = int(vals[1])
            No_lis   = int(vals[2])
            No_mppys = int(vals[3])
            No_tfsis = int(vals[4])
            sys.stderr.write('# Number of peos, Number of monomers, Lis, MPPYs, TFSIs: '+str(No_peos)+' '+str(No_mms)+' '+str(No_lis)+' '+str(No_mppys)+' '+str(No_tfsis)+'\n')

filename = sys.argv[carg]
carg +=1
tdis = float(sys.argv[carg])
carg +=1

    
#################################################################################
""" reading data file """
#################################################################################
f = open(filename)
data = f.readlines()
f.close()
List = []
for j in range(0, len(data)):
    if not (data[j].startswith("#") or data[j].startswith("\n")) :
            tmp = fromstring(data[j],sep=" ")
            #print len(tmp)
            List.append(tmp)
            
sys.stderr.write('# import '+filename+' size-'+str(len(List))+'\n')
l = array(List)
No_rows = len(l)
No_columns = len(l[0])

#for i in range(0, No_rows):
#for j in range(0, No_columns):
#    print l[i][j],
#print

#################################################################################
""" computing tau3 """
#################################################################################
min  = 0.0
ival=int(l[No_rows-1][0]-l[0][0]+1)
max = float(ival)

# store all tau3 without any condition
histwoc = Histogram(min, max, ival) 
woc_sum = 0.0
woc_sum2 = 0.0
woc_count = 0.0

# store tau3 if it is greater than tdis
hist = Histogram(min, max, ival)
tot_sum = 0.0
tot_sum2 = 0.0
sum_count = 0.0

tf = [ [ 0.0 for i in range(No_peos) ] for j in range(No_lis) ]

sys.stderr.write('# '+str(No_rows)+' '+str(No_rows/No_lis)+'\n')
sys.stderr.write('# Storing information in tau3-t-'+str(l[No_rows-1][0])+'.dat ... \n')
pout = open("tau3-t-"+str(l[No_rows-1][0])+".dat", 'w')
print >> pout, '# Reading filename: ',filename
print >> pout, '# tmin tmax discard = ',l[0][0],' ',l[No_rows-1][0],' ',tdis

print "# ts  tau3  Li+  old hosts new hosts" 

for i in range(No_lis):
   
    ts = 0
    hosts_ts = [ 0.0 for k in range(No_columns-2) ]   # peo hosts at time ts
    hosts_t  = [ 0.0 for k in range(No_columns-2) ]   # peo hosts at time t
    No_hosts = []
    t=i
    
    while(t<No_rows):
        
        if ts == 0:
            ts = l[t][0]
            for j in range(2, No_columns):
                hosts_ts[j-2] = l[t][j]
                if l[t][j] != 0 :
                    No_hosts.append(j-2)  
            
            # print ts, i, No_hosts           
                    
        else :
            
            No_old = []      # no longer a host 
            No_new = []      # new hosts 
            for j in range(2, No_columns):
                hosts_t[j-2] = l[t][j]
                
                if l[t][j]==0 and  hosts_ts[j-2]!=0:
                    No_old.append(j-2)
                    
                if l[t][j]!=0 and  hosts_ts[j-2]==0:
                    No_new.append(j-2)
                    
            
            if len(No_old)==len(No_hosts) and len(No_new) > 0:   
                tau3 = l[t][0] - ts

                woc_sum += tau3
                woc_sum2 += tau3*tau3
                woc_count += 1
                histwoc.store(tau3)
    
                if tau3 > tdis :
                    tot_sum += tau3
                    tot_sum2 += tau3*tau3
                    sum_count += 1
                    hist.store(tau3)

                #if tau3<2.0 :
                # print ts, tau3, i, No_hosts, No_new
                
                ts=l[t][0]

                # copyig current hosts
                for j in range(No_columns-2):
                    hosts_ts[j] = hosts_t[j]

                No_hosts = []
                for j in range(len(No_new)):
                    No_hosts.append(No_new[j])
            
            
            elif l[t][0]==l[No_rows-1][0]:
                tau3 = l[t][0] - ts

                woc_sum += tau3
                woc_sum2 += tau3*tau3
                woc_count += 1
                histwoc.store(tau3)
                
                if tau3 > tdis :
                    tot_sum += tau3
                    tot_sum2 += tau3*tau3
                    sum_count += 1
                    hist.store(tau3)

                #if tau3<2.0 :
                #print ts, tau3, i, No_hosts, No_new          


        t += No_lis


tau3woc = woc_sum/woc_count
error3woc =  sqrt((woc_sum2/woc_count) - (woc_sum/woc_count)**2)
histwoc.normalize()

tau3 = tot_sum/sum_count
error3 =  sqrt((tot_sum2/sum_count) - (tot_sum/sum_count)**2)
hist.normalize()

print >> pout, '# nb. of events = ', sum_count, woc_count 
print >> pout, '# tau3 = ', tau3,'+-', error3,'ns',  tau3woc,'+-', error3woc,'ns'  

for i in range(hist.N):
    # print >> pout, i*hist.dx+min, " ", hist.rho[i], " ", histwoc.rho[i]
    print >> pout, (i+0.5)*hist.dx+min, " ", hist.rho[i], " ", histwoc.rho[i]

pout.close()
sys.stderr.write('!! Done !! \n')
