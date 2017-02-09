from scipy import *
import matplotlib.pyplot as plt
import numpy.random as nr

def ising_mc(J=1.,Nx=16,Ny=16,nsteps=50000):
    #initial the square lattice
    #define the boundary condistion of this square
    #produce ghost cell on the boundary of the lattice
    S=ones((Nx+2,Ny+2))
    N=Nx*Ny
    T=linspace(1/J,3.5/J,30)
    def MCMC(S,Temp):
        #the 3D matrix used to store the changing of lattice spin information,
        #i.e. record of markov chain
        #only take account of the information after it runs for nsteps/2
        MC_S=zeros((Nx,Ny,nsteps/2))
        #for E, we still need boudary information in the avg state
        #so call it as a larger version of Markov chain of spin information
        MC_SL=zeros((Nx+2,Ny+2,nsteps/2))
        for i in range(nsteps):
            a=nr.randint(0,N)
            xi=int(a/Ny)+1 # +1 is because of the ghost cell on the boundary
            yi=a-int(a/Ny)*Ny+1
            S[xi,yi]=-S[xi,yi]
            Q=-((J/Temp)*(S[xi-1,yi]+S[xi,yi-1]+S[xi+1,yi]+S[xi,yi+1]))*(2*S[xi,yi])
            if Q>0:
                b=nr.uniform()
                if b>=exp(-Q):
                    S[xi,yi]=-S[xi,yi]  #flip back to the origin state, i.e, failed to change state
            # redefine the boundary condition
            S[0]=S[Nx];S[Nx+1]=S[1];S[:,0]=S[:,Ny];S[:,Ny+1]=S[:,1]
            if i >=nsteps/2:
                MC_S[:,:,i-nsteps/2]=S[1:Nx+1,1:Ny+1]
                MC_SL[:,:,i-nsteps/2]=S
        return MC_S,MC_SL

    def Avg(Temp):
        #MC_ST is used to store information for different Temperture
        MC_ST=zeros((Nx,Ny,nsteps/2))
        MC_SLT=zeros((Nx+2,Ny+2,nsteps/2))
        MC_ST,MC_SLT=MCMC(S,Temp)
        M=zeros(nsteps/2)
        E=zeros(nsteps/2)
        for j in range(0,int(nsteps/2)):
            M[j]=(1/N)*(sum(MC_ST[:,:,j]))
            EE=0
            for i in range(N):
                xi=int(i/Ny)+1 # +1 is because of the ghost cell on the boundary
                yi=i-int(i/Ny)*Ny+1
                E_part=-J*MC_SLT[xi,yi,j]*(MC_SLT[xi-1,yi,j]+MC_SLT[xi+1,yi,j]+MC_SLT[xi,yi-1,j]+MC_SLT[xi,yi+1,j])
                EE+=E_part
            E[j]=EE
        Avg_M=(2/nsteps)*(sum(M))
        Avg_M2=(2/nsteps)*(sum(M**2)) #M**2 here is the square of each element of M
        Avg_E=(2/nsteps)*(sum(E))
        Avg_E2=(2/nsteps)*(sum(E**2))
        return Avg_M, Avg_M2,Avg_E,Avg_E2,E

    M_T=zeros(len(T))
    M2_T=zeros(len(T))
    E_T=zeros(len(T))
    E2_T=zeros(len(T))
    C_B=zeros(len(T))
    C_B2=zeros(len(T))
    X_m=zeros(len(T))
    Estate_T0=zeros(nsteps/2)
    Estate_T0=Avg(2.4/J)[4]
    def re_weighting(T1):
        #A1=E
        A1=Estate_T0
        Avg_A1=sum(Estate_T0*exp(-(1/T1-J/2.4)*Estate_T0))/sum(exp(-(1/T1-J/2.4)*Estate_T0))
        A2=Estate_T0**2
        Avg_A2=sum(A2*exp(-(1/T1-J/2.4)*Estate_T0))/sum(exp(-(1/T1-J/2.4)*Estate_T0))

        return (Avg_A2-Avg_A1**2)/T1


    for i in range(len(T)):
        M_T[i],M2_T[i],E_T[i],E2_T[i],_=Avg(T[i])
        C_B[i]=(E2_T[i]-E_T[i]**2)/T[i]
        X_m[i]=M2_T[i]-M_T[i]**2
        C_B2[i]=re_weighting(T[i])

    plt.subplot(311)
    plt.plot(T,M_T)
    plt.xlabel('Temperture')
    plt.ylabel('Avg_M')
    plt.subplot(312)
    plt.plot(T,C_B)
    plt.plot(T,C_B2)
    plt.xlabel('Temperture')
    plt.ylabel('C_B')
    plt.subplot(313)
    plt.plot(T,X_m)
    plt.xlabel('Temperture')
    plt.ylabel('X_m')
    plt.show()


ising_mc()

#comments:
#the magnetization is decreasing as tempertaure goes down
#the heat capacity C_B is growing to a large number and then decrease to a intermidern value
#the magnetic susceptibility also behavior similar as the heat capacity,
# increase and then decrease to a intermidern  value
