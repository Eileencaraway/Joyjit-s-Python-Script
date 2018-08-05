#! /usr/bin/env python

import sys
import os
import StringIO
import numpy as np
from math import pi
pathdir = os.environ['HOME']+'/lammps-9Dec14/analysis_code'
sys.path.append(pathdir) 
from coarseGraining import *

##################################################################################
# compute curl of a 2D vector field 
# curl A = [d/dx(A_y) - d/dy(A_x)]k^hat 
##################################################################################
def getCurlOfAVector(L,Ax,Ay):
    [Nx,Ny]     = np.shape(Ax)
    prefx       = 2*pi/L[0]
    prefy       = 2*pi/L[1]
    Axhat       = np.fft.fft2(Ax)
    Ayhat       = np.fft.fft2(Ay)
    #print "# cg variables:", Axhat.min(), Axhat.max(), np.mean(Axhat), np.std(Axhat)
    #print "# cg variables:", Ayhat.min(), Ayhat.max(), np.mean(Ayhat), np.std(Ayhat)
    #print np.shape(Axhat)
    curlAhat    = np.zeros(np.shape(Ayhat), dtype=complex)

    for m in range(Nx):
        ikx = prefx*m*1j
        #if m>Nx/2:
        #    ikx = prefx*(m-Nx)*1j
        for n in range(Ny):
            iky            = prefy*n*1j
            #if n>Ny/2:
            #    iky = prefy*(n-Ny)*1j
            curlAhat[m][n] = ikx*Ayhat[m][n]-iky*Axhat[m][n]
    curlA = np.real(np.fft.ifft2(curlAhat))/(Nx*Ny)

    return curlA 


l  = [4.,4.]
sx = np.random.random((252,252))
sy = np.random.random((252,252))
(nx,ny) = np.shape(sx)
dx = l[0]/nx
dy = l[1]/ny

for i in range(nx):
    x=(i+0.5)*dx 
    for j in range(ny):
        y=(j+0.5)*dy 
        sx[i][j]=0#-y
        sy[i][j]=x

cs = getCurlOfAVector(l,sx,sy)
print "# cg variables:", sx.min(), sx.max(), np.mean(sx), np.std(sx)
print "# cg variables:", sy.min(), sy.max(), np.mean(sy), np.std(sy)
print "# cg variables:", cs.min(), cs.max(), np.mean(cs), np.std(cs)
writeBinary(sx, 'Ax')
writeBinary(sy, 'Ay')
writeBinary(cs, 'curl')
