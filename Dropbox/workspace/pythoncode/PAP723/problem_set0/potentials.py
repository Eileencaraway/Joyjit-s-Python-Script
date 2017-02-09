from scipy import *
import matplotlib.pyplot as plt

## Return the potential at measurement point X, due to particles
## at position xc and charges qc. xc ,qc and X must be 1D arrays,
## with xc and qc of equal length. The return value is an array
## of the same length as X, containing the potentials at each X point.

def potential(xc,qc,X):
    M=len(X)
    N=len(xc)
    phi=zeros(M)
    for j in range(N):
        phi=phi+qc[j]/abs(X- xc[j])
        return phi

x= array([0.2,-0.2])   ## i don't understand
q= array([1.5,-1.0])
XX=linspace(-3,3,500)  #need they be different name?

phi=potential(x,q,XX)

plt.plot(XX,phi)
pmin,pmax= -50,50  #set the value at the same time
plt.ylim(pmin,pmax)
plt.show()
                   




