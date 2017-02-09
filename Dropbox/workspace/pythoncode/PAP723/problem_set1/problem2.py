from scipy import *
import matplotlib.pyplot as plt
#import problem1
import scipy.linalg as lin
 
def harper_hamiltonian(N,W,phi,alpha):
    H=zeros((N,N))
    for i in range(N):
        H[i,i]=W*cos(2*pi*alpha*i+phi)
    for j in range(N-1):
        H[j+1,j]=1
        H[j,j+1]=1
    return H
 
#print(harper_hamiltonian(6,2,1.45,0.1))

 
def harper_levels_plot(N=199,W=2.,phi=0):
    anum=500
    alpha=linspace(-1,1,anum)
    #print(alpha)
    E=zeros((anum,N))
    for i in range(anum):
        H=harper_hamiltonian(N,W,phi,alpha[i])
        E[i]=lin.eigvalsh(H)
   
    for j in range(N):
        #plt.plot(alpha,E[:,j])
        plt.scatter(alpha,E[:,j],s=1)
    #print(E[:,0]) n=0 should be the ground state Energy

    plt.xlabel('alpha')
    plt.ylabel('energy')
    plt.show()


#harper_levels_plot()
# it seems i should change the code a little bit, this is not exactly what prof want.

def harper_wavefunction_demo(N=199,alpha=1.618034,phi=0.):
    NN=linspace(0,199,199)
    def harper_wavefunction_case(W,N=199,alpha=1.618034,phi=0.):
        H=harper_hamiltonian(N,W,phi,alpha)
        V,M=lin.eigh(H)
        #print(V[0])
        #print(M[:,0])
        P=abs(M[:,0])**2
        return P
    
    P1=harper_wavefunction_case(W=1.2)
    plt.subplot(221)
    plt.plot(NN,P1)
    plt.xlabel('position n')
    plt.ylabel('probability')
    plt.title('W=1.2')
    P2=harper_wavefunction_case(W=1.8)
    plt.subplot(222)
    plt.plot(NN,P2)
    plt.xlabel('position n')
    plt.ylabel('probability')
    plt.title('W=1.8')
    P3=harper_wavefunction_case(W=1.99)
    plt.subplot(223)
    plt.plot(NN,P3)
    plt.xlabel('position n')
    plt.ylabel('probability')
    plt.title('W=1.99')
    P4=harper_wavefunction_case(W=2.2)
    plt.subplot(224)
    plt.plot(NN,P4)
    plt.xlabel('position n')
    plt.ylabel('probability')
    plt.title('W=2.2')

    
    plt.show()
    

#harper_wavefunction_demo()
#W=1.2 the probably to see the particle in different place is distributed center
# of 100, and decrease gradually. 
#after w>~2 the probably to see the particle in a certain place is much higher
# than other location.
# when w larger than 2.2, basically (P>0.75) the particle is restricted around n=72

def harper_ipr_demo(N=199,alpha=1.618034,phi=0.):
    W=linspace(1.2,2.5,14)
    IRP=zeros(14)
    #print(W)
    def harper_ipr_case(W,N=199,alpha=1.618034,phi=0.):
        H=harper_hamiltonian(N,W,phi,alpha)
        V,M=lin.eigh(H)
        IRP=sum(abs(M[:,:])**4)/199
        return IRP
    for i in range(len(W)):
        IRP[i]=harper_ipr_case(W[i])
        
    plt.plot(W,IRP)
    plt.xlabel('W')
    plt.ylabel('IRP')
    plt.title('harper_ipr_demo')
    plt.show()

#harper_ipr_demo()
#IPR is large for localized states. the critial W is around 1.9

def harper_phi_demo(N=199,alpha=0.6,W=2):
    phi=linspace(-pi,pi,20)
    NN=linspace(0,N,N)
    #print(phi)
    E=zeros((N,len(phi)))
   
    for i in range(len(phi)):
        H=harper_hamiltonian(N,W,phi[i],alpha)
        V,M=lin.eigh(H)
        E[:,i]=V
        
    #when phi=-2. try to get the E of red line
    for i in range(N):
        if -1.5<E[i,7]<-0.5:
            #print(E[i,:])
            #print(i)
            Estates=i  #record one out of band state
            
    for i in range(N):
        if 0.5<E[i,6]<1.5:
            #print(E[i,:])
            #print(i)
            Estates2=i  #record one out of band state #119

            
    plt.subplot(221)
    for i in range(N):
        plt.plot(phi,E[i,:])
    plt.xlabel('phi')
    plt.ylabel('energy states')

    plt.subplot(222)
    H=harper_hamiltonian(N,W,phi[1],alpha)
    V,M=lin.eigh(H)
    P=abs(M[:,Estates])**2
    plt.plot(NN,P)
    #E 79

    plt.subplot(223)
    H=harper_hamiltonian(N,W,phi[1],alpha)
    V,M=lin.eigh(H)
    P=abs(M[:,81])**2
    plt.plot(NN,P)
    

    plt.subplot(224)
    H=harper_hamiltonian(N,W,phi[1],alpha)
    V,M=lin.eigh(H)
    P=abs(M[:,Estates2])**2
    plt.plot(NN,P)
    #E=119
    
    plt.show()

#harper_phi_demo()
# alpha=0.6
#for the in-band states, the probablity of particle is distributed
#while for the out-of-band states, it is more localized in certain place.

#for some alpha, there are more bands, the energy states are more distributed
#for some alpha,like alpha=2.0 it only exist one band and no out-of-band states
#for those similar case like what showed above, the characteristic of in-band
#and out-of-band states is the same 


    
    
