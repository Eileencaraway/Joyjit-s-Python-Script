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

Let's define a time window tw = te-ts ; ts: starting time and te = finishing time 
of the file.
Only the two events are considered to calculate td:

i. Li jumps time tj to a polymer chain > ts and departure time tf < te and 
   td = tf-tj > 1ns

ii. a Li resides on a polymer chain throughout the time window ; then 
   td = tw = te-ts
"""
#####################################################################################
#####################################################################################

L = size(sys.argv)
if(L<2) :
    sys.stderr.write('Usage : i. filename')
    print 
    exit()


carg =1
"""
for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-hist":
            carg += 1
            min = float(sys.argv[carg])
            carg +=1
            max = float(sys.argv[carg])
            carg +=1
            ival = float(sys.argv[carg])
            carg +=1
"""
filename = sys.argv[carg]
carg +=1
    
#################################################################################
""" detecting number of peo chains connected with a Li ion during td """
#################################################################################
def detectPEOs(arr,ti,tf):
    nbs = 0
    chain = [0.0, 0.0]
    t=ti
    while(t<tf+27):
        count = 0
        for i in range(2, 12): # nb. of peos
            if arr[t][i] > 0 :
                count += 1
       
        if count == 1:
            chain[0] += 1
        if count == 2:
            chain[1] += 1

        t += 27

    if chain[0]*27/(tf-ti) > 0.9499:
        nbs = 1 

    if chain[1]*27/(tf-ti) > 0.9499:
        nbs = 2 

    return nbs



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
min  = 1.0
max  = l[No_rows-1][0]-l[0][0]
ival = 200
hist = Histogram(min, max, ival)
hist_1peo = Histogram(min, max, ival)
hist_2peo = Histogram(min, max, ival)
tot_sum = 0.0
tot_sum2 = 0.0
sum_count = 0.0
tot_sum_1peo = 0.0
tot_sum2_1peo = 0.0
sum_count_1peo = 0.0
tot_sum_2peo = 0.0
tot_sum2_2peo = 0.0
sum_count_2peo = 0.0

tf= [ [ 0.0 for i in range(10) ] for j in range(27) ]
discard = 27*100 # discarding the last 1 ns result 
sys.stderr.write('# '+str(No_rows)+' '+str(No_rows-discard)+' '+str(No_rows/27)+'\n')
#print l[No_rows-discard-1][0],'', l[No_rows-discard-1][1]
sys.stderr.write('# Storing information in tau3-t-'+str(l[No_rows-1][0])+'.dat ... \n')

pout = open("tau3-t-"+str(l[No_rows-1][0])+".dat", 'w')
print >> pout, '# Reading filename: ',filename
print >> pout, '# tmin tmax = ',l[0][0],' ',l[No_rows-1][0]
  
for i in range(No_rows-discard):
    for j in range(2, No_columns):

        if (l[i][j]!=0 and l[i][0]>tf[i%27][j-2]): 
            uplim = No_rows/27 - i/27
            #print i, " ", j, " ", uplim, " "
            t=1
            while (t < uplim):
                
                if l[i+27*t][j]== 0: # li index in (j-2)th polymer at tf
                    tf[i%27][j-2]= l[i+27*(t-1)][0] 
                    tau3 = l[i+27*(t-1)][0]-l[i][0]

                    if(l[i][0]>l[0][0] and tau3>1.00):
                        tot_sum += tau3
                        tot_sum2 += tau3*tau3
                        sum_count += 1
                        hist.store(tau3)
                        #print l[i][1],'',l[i][0],'',l[i+27*(t-1)][0],'',l[i][j],'',l[i+27*(t-1)][j],
                        #print i%27,'',j-2,'',tf[i%27][j-2]
                        

                        nb_chains = detectPEOs(l,i,i+27*(t-1))
                            
                        if nb_chains == 1:
                            tot_sum_1peo += tau3
                            tot_sum2_1peo += tau3*tau3
                            sum_count_1peo += 1
                            hist_1peo.store(tau3)
                        
                        if nb_chains == 2:
                            tot_sum_2peo += tau3
                            tot_sum2_2peo += tau3*tau3
                            sum_count_2peo += 1
                            hist_2peo.store(tau3)
                            
                    
                    break
                
                elif (i<27 and t==uplim-1):
                    tf[i%27][j-2]= l[i+27*t][0]
                    tau3 = l[i+27*(t-1)][0]-l[i][0]
                    tot_sum += tau3
                    tot_sum2 += tau3*tau3
                    sum_count += 1
                    hist.store(tau3)
                    #print l[i][1],'',l[i][0],'',l[i+27*t][0],'',l[i][j],'',l[i+27*t][j],
                    #print i%27,'',j-2,'',tf[i%27][j-2]

                    nb_chains = detectPEOs(l,i,i+27*(t-1))
                            
                    if nb_chains == 1:
                        tot_sum_1peo += tau3
                        tot_sum2_1peo += tau3*tau3
                        sum_count_1peo += 1
                        hist_1peo.store(tau3)
                        
                    if nb_chains == 2:
                        tot_sum_2peo += tau3
                        tot_sum2_2peo += tau3*tau3
                        sum_count_2peo += 1
                        hist_2peo.store(tau3)
                            
                t +=1


tau3 = tot_sum/sum_count
error3 =  sqrt((tot_sum2/sum_count) - (tot_sum/sum_count)**2)

tau3_1peo=-1
error3_1peo=-1
if sum_count_1peo > 0:
    tau3_1peo = tot_sum_1peo/sum_count_1peo
    error3_1peo = sqrt((tot_sum2_1peo/sum_count_1peo) - (tot_sum_1peo/sum_count_1peo)**2)

tau3_2peo=-1
error3_2peo=-1
if sum_count_2peo > 0:
    tau3_2peo = tot_sum_2peo/sum_count_2peo
    error3_2peo = sqrt((tot_sum2_2peo/sum_count_2peo) - (tot_sum_2peo/sum_count_2peo)**2)


print >> pout, '# nb. of events [all, 1 chain, 2 chains] = ', sum_count, sum_count_1peo, sum_count_2peo  
print >> pout, '# tau3  [all, 1 chain, 2 chains] = ', tau3,'+-', error3,'ns', tau3_1peo,'+-', error3_1peo,'ns', tau3_2peo,'+-', error3_2peo,'ns' 

hist.normalize()
hist_1peo.normalize()
hist_2peo.normalize()
for i in range(hist.N):
    print >> pout, i*hist.dx+min, " ", hist.rho[i], " ", hist_1peo.rho[i], " ", hist_2peo.rho[i]

pout.close()
sys.stderr.write('!! Done !! \n')
