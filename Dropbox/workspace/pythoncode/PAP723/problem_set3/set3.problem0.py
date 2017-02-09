from scipy import *
import matplotlib.pyplot as plt
from scipy.integrate import quad

#coil_field returns the wrong results for Bx and By.  The problem is
#that the rho_hat in Eq. (0) is NOT [cos(phi), sin(phi), 0].  In the
#integral, the phi denotes the position on the current loop, while
# rho_hat denotes the radial vector pointing to the measurement point.
# They are separate variables!
def coil_field(position, current, radius):
    rho=sqrt(position[0]**2+position[1]**2)
    cos_theta=posituin[0]/rho
    sin_theta=position[1]/rho
    z=array([position[2]])
    A=current*radius/(4*pi)
    def fun(phi,j):
        if j==0:
            return cos_theta*z*sin(phi)/(radius**2+rho**2+z**2-2*rho*radius*sin(phi))**(3/2)
        if j==1:
            return sin_theta*z*sin(phi)/(radius**2+rho**2+z**2-2*rho*radius*sin(phi))**(3/2)
        if j==2:
            return [radius-rho*sin(phi)]/(radius**2+rho**2+z**2-2*rho*radius*sin(phi))**(3/2)


    integ1=quad(fun,0.,2*pi,args=(0))
    # quad return result and err
    integ2=quad(fun,0.,2*pi,args=(1))
    integ3=quad(fun,0.,2*pi,args=(2))

    return A*integ1[0],A*integ2[0],A*integ3[0]

def coil_demo(z,rmax,current,radius,spacing):
    N=100
    rho=linspace(0,rmax,N)

    def function(rho):
        r1=array([rho/sqrt(2),rho/sqrt(2),z-spacing/2]) 
        r2=array([rho/sqrt(2),rho/sqrt(2),z+spacing/2])
        B1=coil_field(r1,current,radius)
        B2=coil_field(r2,current,radius)
        Bz=B1[2]+B2[2]
        Brho=sqrt((B1[0]+B2[0])**2+(B1[1]+B2[1])**2)
        return Bz,Brho

    BBz=zeros(N)
    BBrho=zeros(N)

    for i in range(N):
        BBz[i],BBrho[i]=function(rho[i])


    plt.subplot(211)
    plt.plot(rho,BBz)
    #plt.xlabel('${\r}$')  
    #meet problem in show latex rho here
    plt.xlabel('rho') 
    plt.ylabel('$B_z$')
    plt.subplot(212)
    plt.plot(rho,BBrho)
    plt.xlabel('rho')
    plt.ylabel('$B_{rho}$')
    plt.show()


coil_demo(0.2,2,1,1,0.5)

#comments:
#when z=0, B_rho is always zero
#when R=L,  B_z decrease smoothly around R=1, while B_rho  reach its max at R=1, B_rho goes to 0 around rho=0.5,1.5
#R>L the curve is quite smooth, B_rho didn't touch at 0 
#R<L the curve is very sharp, B_z decrease strongly around R, and B_rho reach to zeros much close to radius 



def coil_demo_2(z,rmax,current,radius,spacing,length):
    N=20
    rho=linspace(0,rmax,N)
    d=length
    def function(rho):
        def fundz(dz,i):
            r1=array([rho/sqrt(2),rho/sqrt(2),z-spacing/2-dz]) #the direction is meaningless
            r2=array([rho/sqrt(2),rho/sqrt(2),z+spacing/2+dz])
            B1=coil_field(r1,current/d,radius)
            B2=coil_field(r2,current/d,radius)
            if i==0:
                Bx=B1[0]+B2[0]
                return Bx
            if i==1:
                By=B1[1]+B2[1]
                return By
            if i==2:
                Bz=B1[2]+B2[2]
                return Bz

        Bx=quad(fundz,0,d,args=(0))
        By=quad(fundz,0,d,args=(1))
        Bz=quad(fundz,0,d,args=(2))

        BB=array([Bx[0],By[0],Bz[0]])

        Brho=sqrt(BB[0]**2+BB[1]**2)

        return BB[2],Brho

    BBz=zeros(N)
    BBrho=zeros(N)

    for i in range(N):
        BBz[i],BBrho[i]=function(rho[i])


    plt.subplot(211)
    plt.plot(rho,BBz)
    plt.xlabel('rho')
    plt.ylabel('B_z')
    plt.subplot(212)
    plt.plot(rho,BBrho)
    plt.xlabel('rho')
    plt.ylabel('B_rho')
    plt.show()

#coil_demo_2(0.2,2,1,1,2,0.1)
