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
The one and only condition for td: td > tdis

** tdis : the discarded time, which will be supplied as an external parameter

---------------------------
The determination of tdis:
----------------------------
The tau3 distribution at T=423K is assumed to be exponential. We fit the tau3(T=423K) 
distribution exponentially and find that for tau3 >= 4ns fit works. Therefore,
we decide tdis(T=423K) = 4ns.

For lower T's:
dn^2 (T, tdis) = dn^2 (T=423K, t=4ns) = 34.8 approx.  
 
"""
#####################################################################################
#####################################################################################

L = size(sys.argv)
if(L<3) :
    sys.stderr.write('Usage : i. filename ii. discard time (ns)')
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
tdis = float(sys.argv[carg])
carg +=1
    
#################################################################################
""" detecting the time when a Li+ returns to the same chain """
#################################################################################
def detectReceiver(arr, pid, ti, tf):

    rcv = [ -1 for i in range(3) ]

    peostates = [ 0 for i in range(10) ]
    for i in range(2, 12):
        if (arr[ti][i] > 0):
            peostates[i-2] = 1
    
    peostates[pid] = 0

    t=ti+27
    while(t<tf):
        for i in range(2, 12):
            if (arr[t][i] > 0 ):
                if( peostates[i-2]==0):
                    
                    #print i-2, '', arr[t][0], '',
                    if (i-2==pid):
                        rcv[0]=1
                    else:
                        rcv[0]=0

                    rcv[1] = i-2 # receivor id  
                    rcv[2] = t
                    break

        t += 27

    #print pid, '', ti, '', arr[ti][0], '', tf, '', rcv_pid
    return rcv

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

# store 1 if a Li+ returns back to the same chain else store 0 at tau3
# store number of events for the above operation   
histrb1 = Histogram(min, max, ival)  
histrb2 = Histogram(min, max, ival)  
rbcount = 0.0
shcount = 0.0

# store tau3 if it is greater than tdis and always connected with a single chain
hist_1peo = Histogram(min, max, ival)
tot_sum_1peo = 0.0
tot_sum2_1peo = 0.0
sum_count_1peo = 0.0

# store tau3 if it is greater than tdis and always connected with double chains
hist_2peo = Histogram(min, max, ival)
tot_sum_2peo = 0.0
tot_sum2_2peo = 0.0
sum_count_2peo = 0.0

tf = [ [ 0.0 for i in range(10) ] for j in range(27) ]
state = [ -1 for i in range(3) ]

sys.stderr.write('# '+str(No_rows)+' '+str(No_rows/27)+'\n')
sys.stderr.write('# Storing information in tau3-t-'+str(l[No_rows-1][0])+'.dat ... \n')
print "# printing information about short events < 1.0 ns ..."
print "# Nb.  state(0/1)  Li+  Donor   Jumped time     tau3"
pout = open("tau3-t-"+str(l[No_rows-1][0])+".dat", 'w')
print >> pout, '# Reading filename: ',filename
print >> pout, '# tmin tmax discard = ',l[0][0],' ',l[No_rows-1][0],' ',tdis
  
for i in range(No_rows):
    for j in range(2, No_columns):
        
        if (l[i][j]!=0 and l[i][0]>tf[i%27][j-2]): 
            uplim = No_rows/27 - i/27
            #print i, " ", j, " ", uplim, " "
            t=1
            while (t < uplim):
                
                if l[i+27*t][j]== 0: # li index in (j-2)th polymer at tf
                    tf[i%27][j-2]= l[i+27*(t-1)][0] 
                    tau3 = l[i+27*(t-1)][0]-l[i][0]
                    woc_sum += tau3
                    woc_sum2 += tau3*tau3
                    woc_count += 1
                    histwoc.store(tau3)
                    
                    state = detectReceiver(l, j-2, i+27*(t-1), No_rows)
                    if (state[0] > -1): 
                        histrb1.storeVal(tau3, state[0])
                        histrb2.store(tau3)
                        
                        if (state[0] > 0): 
                            rbcount += 1
                            #print rbcount, l[i][1], j-2, l[i+27*(t-1)][0], tau3

                        if (tau3 < 1.0):
                            shcount += 1
                            print shcount, state[0], l[i][1], j-2, l[i+27*(t-1)][0], tau3
                            
                    """
                    else:
                    rbcount1 += 1
                    print rbcount1, l[i][1], j-2, l[i+27*(t-1)][0], tau3," : ",
                    """
                    if(tau3>tdis):
                        tot_sum += tau3
                        tot_sum2 += tau3*tau3
                        sum_count += 1
                        hist.store(tau3)
                        #print l[i][1],'',l[i][0],'',l[i+27*(t-1)][0],'',l[i][j],'',l[i+27*(t-1)][j],
                        #print i%27,'',j-2,'',l[i][0],'',tf[i%27][j-2],'',tau3
                        

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
                
                elif (t==uplim-1): 
                    tf[i%27][j-2]= l[i+27*t][0]
                    tau3 = l[i+27*t][0]-l[i][0]

                    woc_sum += tau3
                    woc_sum2 += tau3*tau3
                    woc_count += 1
                    histwoc.store(tau3)

                    if(tau3>tdis):
                        tot_sum += tau3
                        tot_sum2 += tau3*tau3
                        sum_count += 1
                        hist.store(tau3)
                        #print l[i][1],'',l[i][0],'',l[i+27*t][0],'',l[i][j],'',l[i+27*t][j],
                        #print i%27,'',j-2,'',l[i][0],'',tf[i%27][j-2],'',tau3

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


tau3woc = woc_sum/woc_count
error3woc =  sqrt((woc_sum2/woc_count) - (woc_sum/woc_count)**2)

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



histwoc.normalize()
hist.normalize()
nbsrb = histrb1.normalize()
hist_1peo.normalize()
hist_2peo.normalize()

print >> pout, '# nb. of events [both, 1 chain, 2 chains, both wo constrain] = ', sum_count, sum_count_1peo, sum_count_2peo, woc_count 
print >> pout, '# tau3  [both, 1 chain, 2 chains, both wo constrain] = ', tau3,'+-', error3,'ns', tau3_1peo,'+-', error3_1peo,'ns', tau3_2peo,'+-', error3_2peo,'ns',  tau3woc,'+-', error3woc,'ns'  

print >> pout, "# Column 6: Distribution of a Li+ to go back to the same chain after the first jump "

print >> pout, "# Column 7: Probability of a Li+ to go back to the same chain after the first jump :", rbcount, "forward-backward jumps out of", nbsrb, "events"

for i in range(hist.N):
    print >> pout, i*hist.dx+min, " ", hist.rho[i], " ", hist_1peo.rho[i], " ", hist_2peo.rho[i], " ", histwoc.rho[i], " ", histrb1.n[i]/rbcount, " ",

    ratio = 0
    if (histrb2.n[i]>0):
        ratio = histrb1.n[i]/histrb2.n[i]
        
    print >> pout, ratio 

pout.close()
sys.stderr.write('!! Done !! \n')
