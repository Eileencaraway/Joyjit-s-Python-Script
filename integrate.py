#! /usr/bin/env python

import sys
import os
import StringIO
import numpy as np
import scipy.integrate as integrate
import scipy.special as special


#####################################################################################
#####################################################################################
"""
The script:
"""
#####################################################################################

def f(r, a0, a1):
    sroot2piinv = 1.0/a0/np.sqrt(2*np.pi) 
    return (sroot2piinv/r)*np.exp( -0.5*(np.log(r/a1))**2/sigma/sigma )

def F(q,r):
    qr=q*r
    return 3.0*(np.sin(qr)-qr*np.cos(qr))/qr**3

def V(r):
    return 4*np.pi*r**3/3.0


################################################################################
"""  reading command pad arguments """
################################################################################
sigma=1
r0   =1
q    =1
const=1
carg =1
if len(sys.argv)<2:
    sys.stderr.write("Usage: lower limit,  upper limit ")
    print
    sys.exit()
    
ll    = float(sys.argv[carg]) # lower limit of the integration
carg += 1
ul    = float(sys.argv[carg]) # upper limit of the integration
carg += 1
################################################################################


################################################################################
"""  performing integration """
################################################################################
function = lambda r: f(r,sigma,r0)*(V(r)**2)*(F(q,r)**2)
I        = integrate.quad(function, ll, ul)
print const*I[0], I[1]
################################################################################
