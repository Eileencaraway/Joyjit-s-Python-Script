from scipy import *
import matplotlib.pyplot as plt

## return the potential at measurement points X, due to particles
## at positions xc and charges qc. xc, qc and X must be 1D arrays,
## with xc and qc of equal length. the return value is an array
## or the same length as X, containing the potentials at each X point.

def potential(xc, qc,X,radius=5e-2):
    assert xc.ndim == qc.ndim ==X.ndim==1  #check xc,qc,X are 1D array
    assert len(xc) == len(qc)
    assert radius > 0.  

    phi= zeros(len(X))
    for j in range(len(xc)):
        dphi= qc[j]/abs(X-xc[j])
        dphi[abs(X-xc[j])<radius] = qc[j]/radius  #
        phi+=dphi
    return phi  # 

##plot the potential produced by N particles of charge 1, distributed
## randomly between x=-1 and x=1.

def potential_demo(N=20):
    X= linspace(-2.0,2.0,200)
    qc=ones(N)
    from scipy.stats import uniform  #
    xc=uniform(loc=-1.0, scale=2.0).rvs(size=N) #

    phi= potential(xc,qc,X)
    fig_label='Potential from' +str(N)+ 'particles'
    plt.plot(X,phi,'ro',label= fig_label)
    plt.ylim(0,1.25* max(phi))
    plt.legend()
    plt.xlabel('r')
    plt.ylabel('phi')
    plt.show()

potential_demo(100)

    
