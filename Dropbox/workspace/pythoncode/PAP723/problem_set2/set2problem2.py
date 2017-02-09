from scipy import *
import matplotlib.pyplot as plt
import scipy.sparse as sp
import scipy.sparse.linalg as spl



def schrodinger_2D(xspan,yspan,Vfun,neigs,E0):
    xmin,xmax,Nx=xspan
    ymin,ymax,Ny=yspan
    xx=linspace(*xspan)
    yy=linspace(*yspan)
    XX,YY=meshgrid(xx,yy)
    #no matter Nx= or =/Ny the shape of this matrix is still a square.
    #Ny decide the shape of the small square, but Nx decide how many small square
    N=Nx*Ny
    #this is the size of the big matrix
    x=reshape(XX,N)
    y=reshape(YY,N)

    h1=(xmax-xmin)/(Nx-1)
    h2=(ymax-ymin)/(Ny-1)
 
    diag0= -2*ones(N)*(1/2)*(1/(h1**2)+1/(h2**2))
    diag1=(1/(2*h1**2))*ones(N)
    diag2=(1/(2*h2**2))*ones(N)
    A=sp.dia_matrix(([diag1,diag2,diag0,diag2,diag1],[-Ny,-1,0,1,Ny]),shape=(N,N)).tocsc()
    #A = sp.csc_matrix(A)
    
    for i in range(1,Nx):   
        A[Ny*i-1,Ny*i]=0
        A[Ny*i,Ny*i-1]=0
        


    V=sp.dia_matrix(([Vfun(x,y)],[0]),shape=(N,N)).tocsc()
    #V=sp.csc_matrix(V)
    #V=sp.dia_matrix(([Vfun(x,y)],[0]),shape=(N,N))
    H= -A+V 

    
    

    E,psi= spl.eigsh(H,k=neigs, sigma=E0)
    #need to reshape this array
    p=reshape(psi,(Nx,Ny,neigs))

    return E, p, x ,y



def elliptical_well_wavefunctions_demo(L=5.0,V0=-20.0,sigx=1.0,sigy=0.5):
    xspan=(-L/2,L/2,100)
    yspan=(-L/2,L/2,100)
    
    def Vfun(x,y): #x, y are array of the same shape
        V=zeros(len(x))
        for i in range(len(x)):
            V[i]= V0*exp(- x[i]**2/(2*sigx**2)- y[i]**2/(2*sigy**2))
        return V
    #when this function is written inside another function
    #it can use the parameter stated outside of this function

    ENERGY,phi,x,y=schrodinger_2D(xspan,yspan,Vfun,9,V0)
    #print(Energy)
    #print(phi)   

    x=reshape(x,(xspan[2],yspan[2]))
    y=reshape(y,(xspan[2],yspan[2]))
    #XX,YY=meshgrid(xx,yy)
    plt.subplot(331)
    plt.pcolormesh(x,y,abs(phi[:,:,0])**2)
    plt.subplot(332)
    plt.pcolormesh(x,y,abs(phi[:,:,1])**2)
    plt.subplot(333)
    plt.pcolormesh(x,y,abs(phi[:,:,2])**2)
    plt.subplot(334)
    plt.pcolormesh(x,y,abs(phi[:,:,3])**2)
    plt.subplot(335)
    plt.pcolormesh(x,y,abs(phi[:,:,4])**2)
    plt.subplot(336)
    plt.pcolormesh(x,y,abs(phi[:,:,5])**2)
    plt.subplot(337)
    plt.pcolormesh(x,y,abs(phi[:,:,6])**2)
    plt.subplot(338)
    plt.pcolormesh(x,y,abs(phi[:,:,7])**2)
    plt.subplot(339)
    plt.pcolormesh(x,y,abs(phi[:,:,8])**2)
    plt.show()

elliptical_well_wavefunctions_demo()

    

def ellipyical_well_energy_depth_plot(L,Vspan,sigx=1.0,sigy=0.5,neigs=20):
    xspan=(-L/2,L/2,100)
    yspan=(-L/2,L/2,100)
    xx=linspace(*xspan)
    yy=linspace(*yspan)
    XX,YY=meshgrid(xx,yy)
    #no matter Nx= or =/Ny the shape of this matrix is still a square.
    #Ny decide the shape of the small square, but Nx decide how many small square
    N=len(xx)*len(yy)
    #this is the size of the big matrix
    x=reshape(XX,N)
    y=reshape(YY,N)
    
    V0=linspace(*Vspan)
    M=Vspan[2]
    EE=zeros((neigs,Vspan[2]))
    #is it alright to define the Vfun again?
    for j in range(len(V0)):
        def Vfun(x,y): #x, y are array of the same shape
            V=zeros(len(x))
            for i in range(len(x)):
                V[i]= V0[j]*exp(- x[i]**2/(2*sigx**2)- y[i]**2/(2*sigy**2))
            return V
        
        EE[:,j],phi,x,y=schrodinger_2D(xspan,yspan,Vfun,neigs,-20.)
        #define the xspan and x for two time , weird here
        
    for j in range(neigs):
        plt.scatter(V0,EE[j])
    plt.title('ellipyical_well_energy_depth_plot')
    plt.xlabel('V0')
    plt.ylabel('E')
    plt.show()
    
Vspan=(-20.,-5.,10)
ellipyical_well_energy_depth_plot(5.0,Vspan)
#as compared with problem 0(b), the number of energy states are both decreased as V goes to 0
#but in this question, the energy is more concertrated around 0,
#while the energy states of 0(b) is more concertrated around V0.



def Vfun2(x,y): #x, y are array of the same shape
    V=zeros(len(x))
    return V



def schrodinger_2D_error_demo(Lx=1.0,Ly=1.0):
    

    NN=array([  20,25,30,35,  40,45,50,55,   60,   80,  100,  120,  140,  160,  180,  200])
    print(NN)
    def numerical(N):
        xspan=(-Lx/2,Lx/2,N)
        yspan=(-Ly/2,Ly/2,N)
        Energy,phi,x,y=schrodinger_2D(xspan,yspan,Vfun2,3,-20)
        return Energy
    
    E=zeros((len(NN),3))
    
    for i in range(len(NN)):
        print(numerical(NN[i]))
        E[i]=numerical(NN[i])
    EA=array([pi**2,2.5*pi**2,2.5*pi**2])
   
    #E 0,1,2
    eps=zeros((3,len(NN)))
    for j in range(3):
        for i in range(len(NN)):
            eps[j,i]= abs(E[i,j]-EA[j])
        
    plt.subplot(311)
    x0=polyfit(log(NN),log(eps[0]),1)
    plt.plot(NN,eps[0],label='ground state %.5f'%x0[0])
    plt.xlabel('N')
    plt.legend()
    
    plt.subplot(312)
    x1=polyfit(log(NN),log(eps[1]),1)
    plt.plot(NN,eps[1],label='energy 1 state %.5f'%x1[0])
    plt.legend()
    
    plt.subplot(313)
    x2=polyfit(log(NN),log(eps[2]),1)
    plt.plot(NN,eps[2],label='energy 2 state %.5f'%x2[0])
    plt.legend()

    plt.show()
        

    
schrodinger_2D_error_demo()
#the error scale with 1/N,
#reason:


        
        
    
    
    
