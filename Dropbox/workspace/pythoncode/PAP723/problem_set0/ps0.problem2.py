from scipy import *
import matplotlib.pyplot as plt

#this function is used to produce each step randomly
def stepfun():
    x=array([[1.0,0.0],[-1.0,0.0],[0.0,-1.0],[0.0,1.0]])
    return x[random.randint(0,4)]

# r size is  1*2
# walkr size is n*2
def random_walk_plot(stepfun,nsteps):
    r=array([0.,0.])
    walkr=zeros((nsteps,2))
    for i in range(nsteps):
        walkr[i]=r
        r+=stepfun()

    plt.plot(walkr[:,0],walkr[:,1])
    #plt.axis([-100.,100.,-100.,100.])  # this should be array
    #this hard-coding of +/-100 is error prone
    plt.show()
    #return walkr[-1]   # r lead problem


#random_walk_plot(stepfun,1000)
#above is used to test (a)
#print('good')

def random_walk_stats(stepfun,nsteps,nwalks):
    rtotal=array([0.,0.])
    rsquareT=0.

    for j in range(nwalks):
        rn=array([0.,0.])
        for i in range(nsteps):
            rn+=stepfun()
        #rtotal+=(rn[0]**2+rn[1]**2)**(0.5)  #abs?
        rtotal+=rn
        rsquareT+=rn[0]**2+rn[1]**2

    rmean=rtotal/nwalks
    msd=rsquareT/nwalks-(rmean[0]**2+rmean[1]**2)

    return rmean,msd

#print(random_walk_stats(stepfun,100,10000))
#above is used for test (b)


#in this function,each times of random walk have N steps
#and we run for M times
#use random.normal function to produce the random numbers obey gaussian distribution
def random_walk_gaussian_demo(mux=0.1,muy=0.0,sigx=1.0,sigy=1.0):

    M=100
    NN=1000
    N=linspace(1,NN,NN)

    Ravg=zeros(NN)
    rmsd=zeros(NN)
    #print('good1')
    for j in range(NN):
        Rt=array([0.0,0.0])
        r2=0.0
        for i in range(M):
            dx=random.normal(mux,sigx,j+1)
            dy=random.normal(muy,sigy,j+1)

            Rt[0]+=sum(dx)
            Rt[1]+=sum(dy)
            r2+=(sum(dx)**2+sum(dy)**2)


        Ravg[j]=((Rt[0]/M)**2+(Rt[1]/M)**2)**(0.5)
        rmsd[j]=(r2/M)-Ravg[j]**2

    #print(N)
    #print(rmsd)
    x1=polyfit(log(array(N)),log(rmsd),1)
    x2=polyfit(log(array(N)),log(Ravg),1)
    #transfer into log function
    #print(x1)
    #print(exp(x1[1]))
    p=exp(x1[1])*N**(x1[0])
    p2=exp(x2[1])*N**(x2[0])

    #l2=sum((random.normal(mux,sigx,10000))**2+(random.normal(muy,sigy,10000))**2)/10000
    l3=sigx**2+sigy**2
    #print(l2,l3)
    plt.subplot(1,2,1)
    plt.plot(N,Ravg,N,p2)

    plt.subplot(1,2,2)
    plt.plot(N,rmsd)
    plt.plot(N,p)
    plt.text(200, 1500, r'$\alpha=%.5f$'%x1[0]+r'$,D=%.5f$'%x1[1])
    #theoretical speaking, rmsd->Nl^2/6

    #print(l2)
    plt.plot(N,N*l3)
    plt.show()

#random_walk_gaussian_demo()
#another way is to take advantage of the function i wrote in the first and second problem



def levy_flight_demo(N):
    M=100
    rn2m=zeros(M)

    def levy_flight_1(N):
        dr=random.standard_cauchy(N)
        #print(dr)
        theta=random.uniform(-pi,pi,N)
        #print(theta)
        r=array([0.,0.])
        #use walkr to record the steps
        walkr=zeros((N,2))

        for i in range(N):
            walkr[i]=r
            r[0]+=dr[i]*cos(theta[i])
            r[1]+=dr[i]*sin(theta[i])
        #print(walkr)
        plt.subplot(211)
        plt.plot(walkr[:,0],walkr[:,1])
        plt.title('levy_flight')
        plt.axis([-100.,100.,-100.,100.])
        #plt.show()
        return walkr[-1,:]

    #plot M times the levy_flight,thus have an array of rN
    for j in range(M):
        rn=levy_flight_1(N) #the end to end vector
        rn2=rn[0]**2+rn[1]**2 #square of the vector
        rn2m[j]=rn2 #store each time of the square of distance in this array


    bins=[0,100,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,20000]
    plt.subplot(212)
    n,bins,patches=plt.hist(rn2m,bins,normed=0,facecolor='green')
    plt.title('histogram')
    plt.show()


#because sometimes we have a very large dr, one step is very huge
#so we can observe from trajectory of levy flight several long line
#the cauchy function can produce a lot of small numbers and some very big numbers
#if we calculate msd of this, it would be much larger number than gaussion distribution
# it would be infinite prof said.
levy_flight_demo(10)
