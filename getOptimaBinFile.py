#! /usr/bin/env python

import sys
import os
import StringIO
#import numpy
from numpy import *
#from lammpsOperations import *
#from coarseGraining import *
#pathdir = os.environ['HOME']+'/mols/misc_scripts'
#sys.path.append(pathdir) 
#from histogram import *

#################################################################################
#################################################################################
verbose= False
###################################################################################

#######################################################################
def readBinary(fname, verbose=False):
    if verbose:
        sys.stderr.write("# reading file "+fname+'\n')
    readf = open(fname,'rb')
    Nx    = fromfile(readf, 'int32', 1)
    Ny    = fromfile(readf, 'int32', 1)
    data  = fromfile(readf, 'float32').reshape(Nx,Ny)
    readf.close()
    if verbose:
        sys.stderr.write("# cg variables: "+str(data.min())+' '+str(data.max())+' '+str(mean(data))+' '+str(std(data))+'\n')

    return [int(Nx), int(Ny), data]
#######################################################################

###################################################################################
if(size(sys.argv)<2) :
    sys.stderr.write('Usage : i. binary file \n')
    print 
    exit()

carg = 1
for word in sys.argv[carg:]:
    if word[0] == "-":
        if word == "-v": # set colorbar boundary for the cg variable
            verbose = True
            carg += 1

binf  = sys.argv[carg]
carg  += 1
###################################################################################

#########################################
# reading cg bin files
#########################################
[Nx, Ny, data]  = readBinary(binf, verbose)
##############################################################################

##############################################################################
sys.stderr.write('# cg variables: min, max, avg., std. \n')
print data.min(), '    ',  data.max(), '    ', mean(data),'    ', std(data)
