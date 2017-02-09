from scipy import *
import matplotlib.pyplot as plt
import scipy.optimize
import scipy.integrate 
 
def func(E, V0, L):
        Y= tan(sqrt(2.*(E-V0))*L)+sqrt(V0/E -1)
        return Y
     
def solve(Egs,V0,L):
        return scipy.optimize.fsolve(func, Egs, args=(V0,L))
     
def quantum_well_energy_width_plot(Lspan,V0=-2.):
    LN=linspace(*Lspan)
    #print(LN)
    M=20
    EE=zeros((M,10))
     
    for i in range(10):
        #print(V0+ pi**2/(8*LN[i]**2))
        Egs=linspace(V0+ pi**2/(8*LN[i]**2)+0.0000001,-0.00000001,M)
           #when it goes to energy have a trend goes to -2.0 a problem jump out
            #in order to avoid this problem, start guess the e value after
            #the first period of tan, ie sqrt(2.*(E-V0))*L> pi/2
        for j in range(M):
                EE[j,i]=solve(Egs[j],V0,LN[i])
             
    #print(EE)
    for j in range(M):
        plt.scatter(LN,EE[j])
    plt.title('quantum well energy width plot')
    plt.xlabel('L')
    plt.ylabel('Energy')
    plt.show()
    
     
 
Lspan=(1,10,10)
quantum_well_energy_width_plot(Lspan,V0=-2.)

def pre_plot(V0=-8,L=3.):
     
    E=linspace(V0,-0.001,500)
     
    #print(E)
    plt.plot(E,tan(sqrt(2.*(E-V0))*L))
    plt.plot(E,- sqrt(V0/E -1))
    plt.ylim(-10, 10)
    plt.show()
 
 
#pre_plot()
 

def quantum_well_energy_depth_plot(L,Vspan):
    V0=linspace(*Vspan)
    #print(V0)
    M=Vspan[2]
 
    EE=zeros((20,M))
     
    for i in range(M):
        Egs=linspace(V0[i]+ pi**2/(8*L**2)+0.000001,-0.00000001,20)
        #when it goes to energy have a trend goes to -2.0 a problem jump out
        #in order to avoid this problem, start guess the e value after
        #the first period of tan, ie sqrt(2.*(E-V0))*L> pi/2
        for j in range(20):
            EE[j,i]=solve(Egs[j],V0[i],L)
             
    #print(EE)
    for j in range(20):
        plt.scatter(V0,EE[j])

    plt.title('quantum well energy depth plot')
    plt.xlabel('V0')
    plt.ylabel('Energy')
 
    plt.show()
    
Vspan=(-20.,-5.,10)  # v also cannot choose a very small number
LL=5.    
quantum_well_energy_depth_plot(LL,Vspan)
# 
 
def quantum_well_wavefunction_demo():
    L=7
    V=-2.
    Egs=linspace(V+ pi**2/(8*L**2)+0.000001,-0.0000001,20)
    EE=zeros(20)
    for i in range(20):
        EE[i]=solve(Egs[i],V,L)
    #print(EE)
    #try to change this part to make it automatic
    condition=zeros(len(EE))
    condition[0]=True
    for i in range(1,len(EE)):
        if EE[i]-EE[i-1]>0.001:
            condition[i]=True
 
    E=extract(condition,EE)
    #print(len(E))
    #print(E)
    #E=array([EE[0],EE[4],EE[18]])
    #print(E)
 
    def phi(x,E,V,L):
        if x<=0:
            Y=0
        elif  0<x<L:
            Y=sin(sqrt(2.*(E-V))*x)
        else:
            Y=exp(-sqrt(-2*E)*x)
        return Y
 
    XX=linspace(0,10,100)
    
     
    A=zeros(len(E))
    B=zeros(len(E))
    Y=zeros((len(E),100))
    #result= scipy.integrate.quad(lambda x: phi(x,E[0],V,L),-inf,+inf)
    for i in range(len(E)):
            #integrate from 0~L
            #pay attention to the output of integrate.quad
            a,aerr=scipy.integrate.quad(lambda x: phi(x,E[i],V,L)**2,0,L)
 
            #integrate from L~ inf
            b,berr=scipy.integrate.quad(lambda x: phi(x,E[i],V,L)**2,L,+inf)
 
            c=exp(-sqrt(-2*E[i])*L)/sin(sqrt(2.*(E[i]-V))*L)
 
            B[i]=sqrt( 1/((c**2)*a+b))
 
            A[i]=B[i]*c
 
            for j in range(100):
                    if XX[j]<=0:
                         Y[i,j]=0
                    elif 0<XX[j]<L:
                         Y[i,j]=(A[i]*sin(sqrt(2.*(E[i]-V))*XX[j]))**2
                    else:
                         Y[i,j]=(B[i]*exp(-sqrt(-2*E[i])*XX[j]))**2
 
            plt.plot(XX,Y[i])
    plt.title('quantum well wavefunction demo')
    plt.xlabel('X')
    plt.ylabel('probability')
              
 
    plt.show()
     
             
         
 
     
 
quantum_well_wavefunction_demo()
 
def quantum_well_nbound_states():
 
    def bound_states(V,L):
        Egs=linspace(V+ pi**2/(8*L**2)+0.00000001,-0.0000001,20)
        EE=zeros(20)
        for i in range(20):
            EE[i]=solve(Egs[i],V,L)
        #print(EE)
        #try to change this part to make it automatic
        condition=zeros(len(EE))
        condition[0]=True
        for i in range(1,len(EE)):
            if EE[i]-EE[i-1]>0.001:
                condition[i]=True
 
        E=extract(condition,EE)
        return len(E)
    #print(bound_states(-2,1))
    #I think i need to improve my calculation to speed up 
 
    V=linspace(-10,-2,9)
    L=linspace(10,1,10)
    #print(L)
    f=zeros((9,10))
    n=zeros((9,10))
    for j in range(9):
            for i in range(10):
                    f[j,i]=V[j]*L[i]**2
                    
                    n[j,i]=bound_states(V[j],L[i])  
            
  
    #print(f)
    #print(n)
    ff=linspace(-1000,-5,100)
    AS=sqrt(-2*ff)/pi   
    plt.scatter(f,n)
    plt.plot(ff,AS)
    plt.title('quantum well nbound states')
    plt.xlabel('f')
    plt.ylabel('n')
    plt.show()
     
         
quantum_well_nbound_states()
#when V goes to - infinite large, the problem approximate the "particle in a box"
#E=(n**2*pi**2)/(2*L**2) +V0
#E<0 bound states

     
    
