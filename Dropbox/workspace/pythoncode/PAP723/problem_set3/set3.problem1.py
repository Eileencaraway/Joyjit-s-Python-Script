from scipy import *
import matplotlib.pyplot as plt
from scipy.integrate import ode

def vanderpol_plot(x0,v0,t1=500.,nt=2000,mu=100.):
    t=linspace(0,t1,nt)
    y0=array([x0,v0])
    def ydot(t,y,mu):  #pay attention to t,y for ode and y,t for odeint
        x,v= y[0],y[1]
        return array([v,mu*(1-x**2)*v-x])
    

    r = ode(ydot)
    r.set_integrator('dopri5')
    r.set_initial_value(y0)
    r.set_f_params(mu)

    x= zeros(len(t))
    x[0]=y0[0]
    for n in range(1,len(t)):
        r.integrate(t[n])
        assert r.successful()
        x[n]= (r.y)[0]

    
        
    plt.plot(t,x,'b-')
    plt.xlabel('t')
    plt.ylabel('x')
    plt.show()

#vanderpol_plot(2,10)

def vanderpol_profile(dt1=1e-3,dt2=2.,mu=100.):
    
    
    def ydot(t,y):
        nonlocal count
        count=count+1
        x,v= y[0],y[1]
        return array([v,mu*(1-x**2)*v-x])
    
    y0=array([0.,1.])
    #t=linspace(0.,50.,100) #
    N=1000
    dt=linspace(dt1,dt2,N)
    ncount1=zeros(N)
    ncount2=zeros(N)
    x=zeros(len(dt))
    x[0]=y0[0]
    
    for i in range(len(dt)):
        count=0
        r1= ode(ydot)
        r1.set_integrator('dopri5',nsteps=1000)
        r1.set_initial_value(y0)
        r1.integrate(dt[i])
        assert r1.successful()
        ncount1[i]=count

    for i in range(len(dt)):
        count=0
        r2= ode(ydot)
        r2.set_integrator('LSODA')
        r2.set_initial_value(y0)
        r2.integrate(dt[i])
        assert r2.successful()
        ncount2[i]=count
    
   
    dopri5,=plt.plot(dt,ncount1,'b-',label='dopri5')
    LSODA,=plt.plot(dt,ncount2,'r-',label='LSODA')
    plt.legend([dopri5,LSODA],['dopri5','LSODA'])
    plt.xlabel('dt')
    plt.ylabel('n')
    plt.show()

vanderpol_profile()    
    
    
    
