from scipy import *
import matplotlib.pyplot as plt
 
'''def stepfun():
    x=array([[1.0,0.0],[-1.0,0.0],[0.0,-1.0],[0.0,1.0]])
    return x[random.randint(0,4)]
 
# r size is  1*2
# walkr size is n*2
def random_walk_plot(stepfun,nsteps):
    r=array([0.,0.])
    walkr=zeros((nsteps,2))
    for i in range(nsteps):
        walkr[i]=r #when is the situation I can use this?
        r+=stepfun()
         
    plt.plot(walkr[:,0],walkr[:,1])
    plt.axis([-100.,100.,-100.,100.])  # this should be array
    plt.show()
    #return walkr[-1]   # r lead problem
 
 
#random_walk_plot(stepfun,100)  #why it will stop here?
print('good')
 
def random_walk_stats(stepfun,nsteps,nwalks):
    rtotal=array([0.,0.])
    rsquareT=0.
    
    print('good1')
        
    for j in range(nwalks):
        rn=array([0.,0.])
        for i in range(nsteps):
            rn+=stepfun()
        #rtotal+=(rn[0]**2+rn[1]**2)**(0.5)  #abs?
        rtotal+=rn
        rsquareT+=rn[0]**2+rn[1]**2
         
    rmean=rtotal/nwalks
    msd=rsquareT/nwalks-(rmean[0]**2+rmean[1]**2)
    print("good2")
    return rmean,msd
 
print(random_walk_stats(stepfun,1000,10000))''' # now it should be right

def random_walk_gaussian_demo(mux=0.1,muy=0.0,sigx=1.0,sigy=1.0):

    M=100
    N=linspace(0,1000,1000)
    NN=1000
   
    
    Ravg=zeros(NN)
    rmsd=zeros(NN)
    print('good1')
    for j in range(NN):
        Rt=array([0.0,0.0])
        r2=0.0
        for i in range(M):
            dx=random.normal(mux,sigx,NN)
            dy=random.normal(muy,sigy,NN)
        
            Rt[0]+=sum(dx)
            Rt[1]+=sum(dy)
            #r2[0]=r2[0]+(sum(dx)**2+sum(dy)**2)
        
        
        Ravg[j]=((Rt[0]/M)**2+(Rt[1]/M)**2)**(0.5)
        #rmsd[j]=(r2/M)-Ravg[j]**2
        
        
    

    #plt.subplot(1,2,1)
    plt.plot(N,Ravg)
    print('good1')
    #plt.subplot(1,2,2)
    #plt.plot(N,rsd)
    
random_walk_gaussian_demo()
