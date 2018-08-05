#! /usr/bin/env python

import sys
import os
import StringIO
import numpy as np
from scipy import linalg

rm      = 2**(1./6.)
rm2     = rm*rm
rm3     = rm2*rm
rm4     = rm3*rm
rm5     = rm4*rm
rm6     = rm5*rm
rminv   = 1.0/rm
rminv2  = rminv*rminv
rminv6  = rminv2*rminv2*rminv2
rminv7  = rminv6*rminv
rminv8  = rminv7*rminv
rminv12 = rminv6*rminv6
rminv13 = rminv7*rminv6
rminv14 = rminv7*rminv7
print rm, rminv, rminv12 

rc      = 2.4
rc2     = rc*rc
rc3     = rc2*rc
rc4     = rc3*rc
rc5     = rc4*rc
rc6     = rc5*rc
rcinv   = 1.0/rc
rcinv2  = rcinv*rcinv
rcinv6  = rcinv2*rcinv2*rcinv2
rcinv7  = rcinv6*rcinv
rcinv8  = rcinv7*rcinv
rcinv12 = rcinv6*rcinv6
rcinv13 = rcinv7*rcinv6
rcinv14 = rcinv7*rcinv7
print rc, rcinv 

A = np.array([[rminv12, -rminv6, rm6, rm4, rm2, 1], [rcinv12, -rcinv6, rc6, rc4, rc2, 1], [-12*rminv13, 6*rminv7, 6*rm5, 4*rm3, 2*rm, 0], [ -12*rcinv13, 6*rcinv7, 6*rc5, 4*rc3, 2*rc, 0], [ 156*rminv14, -42*rminv8, 30*rm4, 12*rm2, 2, 0], [156*rcinv14, -42*rcinv8, 30*rc4, 12*rc2, 2, 0]])

Ainv = linalg.inv(A)
print Ainv

B = np.array([[4*rminv12-4*rminv6],[0],[-48*rminv13+24*rminv7],[0],[624*rminv14-168*rminv8],[0]])
print B

#X = Ainv.dot(B)
#print 'X= ', X

Y = np.linalg.solve(A, B)
print '#################################################'
print '## For rcut ', rc,', and rmin 2^1/6 --> Coeffs:'
print Y
print '#################################################'

sij  = 1.4
sij2 = sij*sij
sij4 = sij2*sij2
sij6 = sij4*sij2

rij  = rm*sij
rij2 = rij*rij
rij4 = rij2*rij2
rij6 = rij4*rij2
rijinv  = 1./rij
rijinv2 = rijinv*rijinv
rijinv6 = rijinv2*rijinv2*rijinv2
rijinv8 = rijinv6*rijinv2
 
U = 4*sij6*rijinv6*(sij6*rijinv6 - 1)
print 'U1 ', U

U = sij6*rijinv6*(Y[0]*sij6*rijinv6 - Y[1]) + Y[5] + Y[4]*rij2/sij2 + Y[3]*rij4/sij4 + Y[2]*rij6/sij6 
print 'U2 ', U

# -du/dr/r
F = sij6*rijinv6*rijinv2*(48.*sij6*rijinv6 - 24.)
print 'F1 ', F

F = sij6*rijinv6*rijinv2*(Y[0]*12*sij6*rijinv6 - Y[1]*6) - Y[4]*2/sij2 - Y[3]*4*rij**2/sij4 - Y[2]*6*rij**4/sij6
print 'F2 ', F

# d2u/dr2
mu = sij6*rijinv6*rijinv2*(48.*13.*sij6*rijinv6 - 24*7.)
print 'mu1 ', mu

mu = sij6*rijinv6*rijinv2*(Y[0]*156.*sij6*rijinv6 - Y[1]*42.) + Y[4]*2/sij2 + Y[3]*12*rij**2/sij4 + Y[2]*30*rij**4/sij6
print 'mu2 ', mu


rij  = rc*sij

U = sij6*(rij)**(-6.)*(Y[0]*sij6*(rij)**(-6.) - Y[1]) + Y[5] + Y[4]*rij**2/sij2 + Y[3]*rij**4/sij4 + Y[2]*rij**6/sij6 
print 'U at rc ', U

# -du/dr/r
F = sij6*rij**(-6.)*rij**(-2.)*(Y[0]*12*sij6*rij**(-6.) - Y[1]*6) - Y[4]*2/sij2 - Y[3]*4*rij**2/sij4 - Y[2]*6*rij**4/sij6
print 'F2 at rc ', F

# d2u/dr2
mu = sij6*rij**(-6.)*rij**(-2.)*(Y[0]*156.*sij6*rij**(-6.) - Y[1]*42.) + Y[4]*2/sij2 + Y[3]*12*rij**2/sij4 + Y[2]*30*rij**4/sij6
print 'mu at rc', mu

