from scipy import   *
import matplotlib.pyplot as plt
from scipy.integrate import ode
from numpy.fft import fft,fftfreq


def pendulum_sample(theta0,thetadot0,gamma,omega0,Fd,t):



    def ydot(t,y,gamma,omega0,Fd):
        theta,thetadot=y[0],y[1]
        return array([thetadot,Fd*cos(2*pi*t)-sin(theta)*omega0**2-2*gamma*thetadot])
    y0=array([theta0,thetadot0])

    r= ode(ydot)
    r.set_integrator('dopri5',nsteps=1000)
    r.set_initial_value(y0)
    r.set_f_params(gamma,omega0,Fd)

    theta= zeros(len(t))
    thetadot=zeros(len(t))
    theta[0]=y0[0]
    thetadot[0]=y0[1]
    for n in range(1,len(t)):
        r.integrate(t[n])
        assert r.successful()
        #theta[n]= mod(r.y[0],2*pi)
        theta[n]=r.y[0]
        thetadot[n]=r.y[1]


    return theta, thetadot


def pendulum_demo():

    t=linspace(0,10.0,1000)
    Fd=array([0.0,50.,60.,70.,80.])

    for i in range(len(Fd)):
        theta,thetadot=pendulum_sample(1,0.0,0.1,10,Fd[i],t)
        plt.subplot(5,2,2*i+1)
        plt.plot(t,theta)
        plt.subplot(5,2,2*i+2)
        plt.plot(t,thetadot)
        plt.xlabel('time')
        plt.ylabel('thetadot')
    plt.show()

#pendulum_demo()

def pendulum_spectrum_demo():
    theta0=1.0; thetadot0=0.0 ; gamma=0.1; omega0=10.
    N=1000;Maxt=500
    t=linspace(0,Maxt,N)
    T=Maxt/N

    Fd=array([40.,50.,60.,70.,80.])

    for i in range(len(Fd)):
        theta,thetadot=pendulum_sample(theta0,thetadot0,gamma,omega0,Fd[i],t)
        sp=fft(thetadot)
        #freq=fftfreq(t.shape[-1])
        freq=linspace(0,pi/T,N/2)


        plt.subplot(3,2,i+1)
        #plt.plot(freq,abs(sp))
        plt.plot(freq[0:N/20],abs(sp[0:N/20]))
        plt.xlabel('frequence')
        plt.ylabel('amplitude')

    plt.show()


pendulum_spectrum_demo()

#
def pendulum_perturbaltion_demo():
    theta01=1.;theta02=1+1e-8
    thetadot0=0.0
    y01=array([theta01,thetadot0]);y02=array([theta02,thetadot0])
    Fd=linspace(50,55,100)
    gamma=0.1  ;omega0=10;T=50;t0=0.0

    def endstate(F,y0):
        def ydot(t,y,gamma,omega0,F):
            theta,thetadot=y[0],y[1]
            return array([thetadot,F*cos(2*pi*t)-sin(theta)*omega0**2-2*gamma*thetadot])

        r= ode(ydot)
        #r.set_integrator('dopri5',nsteps=10000)
        r.set_integrator('LSODA')
        r.set_initial_value(y0,t0)
        r.set_f_params(gamma,omega0,F)
        dt=0.1
        while r.t<T:
            r.integrate(r.t+dt)
            r.t+=dt
        #assert r.successful()
        #theta[n]= mod(r.y[0],2*pi)
        return r.y[0],r.y[1]

    A=zeros(len(Fd))
    for i in range(len(Fd)):
        theta1,thetadot1=endstate(Fd[i],y01)
        theta2,thetadot2=endstate(Fd[i],y02)
        A[i]=abs(thetadot1-thetadot2)

    plt.plot(Fd,A)
    plt.xlabel('Fd')
    plt.ylabel('change in final state')
    plt.show()

#pendulum_perturbaltion_demo()
# as know from the following question and discuss with classmate, the behavour of the plot 
#should be start to change randomly and strongly after 53
#but i failed to figure out what happened here in my code

def pendulum_turning_points_demo():
    theta0=1.
    thetadot0=0.0
    gamma=0.1  #small dampping?
    omega0=10
    T=50;M=500;N=200
    Fd=linspace(50,80,M)
    t=linspace(0,T ,N)

    def state(F):
        theta=zeros(N)
        thetadot=zeros(N)
        theta,thetadot=pendulum_sample(theta0,thetadot0,gamma,omega0,F,t)
        A=zeros(N,dtype=bool)
        for i in range(int(N/2),N-1):
            if (theta[i]-theta[i-1])*(theta[i+1]-theta[i])<0:
            	A[i]=True

        return theta[A]

    for j in range(M):
        TPtheta=state(Fd[j])  #shape is different, cannot pass through
        TPthetaN=zeros(len(TPtheta))
        for i in range(len(TPtheta)):
        	TPthetaN[i]=mod(TPtheta[i],2*pi)
        #print(state(Fd[j]))
        plt.scatter(ones(len(TPtheta))*Fd[j], TPthetaN,s=1)
        plt.xlabel('Fd')
        plt.ylabel('Theta')
    plt.show()


pendulum_turning_points_demo()

#comment:
# we can see a  horizontal line before 53, it means before 53, the movement of  
#pendulum  still has periodic, 
#while when driven force is larger than 53, 
#it it chaotic.