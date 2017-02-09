from scipy import *
import matplotlib.pyplot as plt


#in this function,each times of random walk have N steps, and we run for M times
#use random.normal function to 
def random_walk_gaussian_demo(mux=0.1,muy=0.0,sigx=1.0,sigy=1.0):
 
    M=100
    NN=1000
    N=linspace(0,NN,NN)
      
    Ravg=zeros(NN)
    rmsd=zeros(NN)
    print('good1')
    for j in range(NN):
        Rt=array([0.0,0.0])
        r2=0.0
        for i in range(M):
            dx=random.normal(mux,sigx,j)
            dy=random.normal(muy,sigy,j)
         
            Rt[0]+=sum(dx)
            Rt[1]+=sum(dy)
            r2+=(sum(dx)**2+sum(dy)**2)
         
         
        Ravg[j]=((Rt[0]/M)**2+(Rt[1]/M)**2)**(0.5)
        rmsd[j]=(r2/M)-Ravg[j]**2
         
         
     
    plt.subplot(1,2,1)
    plt.plot(N,Ravg)
    plt.subplot(1,2,2)
    plt.plot(N,rmsd)
    plt.show()
     
random_walk_gaussian_demo()


