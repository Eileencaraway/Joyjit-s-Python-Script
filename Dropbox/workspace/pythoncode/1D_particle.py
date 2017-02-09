#a particle is moving as a spring -kx in 1D
from scipy import *
import matplotlib.pyplot as plt
from matplotlib import animation

#this function is used to plot the potential well
def potential_plot():
    x=linspace(-5.,5.,100)
    U=zeros(len(x))
    K=1.0
    for i in range(len(x)):
        U[i]=0.5*K*x[i]**2

    plt.plot(x,U)
    plt.show()

#potential_plot()

def MD_simulation():
    T=linspace(0,1,100)
    x0=5.; k=2.;m=1.0
    N=len(T)
    dt=(10.-0)/N

    p=zeros(N);x=zeros(N);f=zeros(N)
    x[0]=x0
    p[0]=0.0
    f[0]=-k*x0
    for i in range(1,N):
        pt=p[i-1]+0.5*dt*f[i-1]
        x[i]=x[i-1]+dt*pt/m
        f[i]=-k*x[i]
        p[i]=pt+0.5*dt*f[i]
        fig=plt.figure(figsize=(10,10))
        plt.plot(x[i],0,'bo')
        plt.xlim([-5.,5.])
        plt.savefig('frame%d.jpg'%i)
        plt.clf()



MD_simulation()
