from scipy import *
import matplotlib.pyplot as plt


def run_and_tumble(N):
    r=array([0.,0.])
    walkr=zeros((N,2))

    def step():
        dr=random.normal(0,0.5)
        #print(dr)
        theta=random.uniform(-pi,pi)
        #print(theta)
        return dr*cos(theta),dr*sin(theta)

    for i in range(N):
        walkr[i]=r
        r+=step()

    plt.plot(walkr[:,0],walkr[:,1])
    plt.title('Run_and_Tumble')
    #plt.axis([-100.,100.,-100.,100.])
    plt.show()

run_and_tumble(100)

#in order to include the diffusion and direction of random walk
#read theory to know how to control the parameters
