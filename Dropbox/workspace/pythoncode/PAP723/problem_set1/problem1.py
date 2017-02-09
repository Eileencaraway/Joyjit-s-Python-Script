from scipy import *
import matplotlib.pyplot as plt
import time
import scipy.linalg
  
def row_reduce(A,b,n):
    N=len(b)
    for i in range(n+1,N):
         
        b[i]=b[i]-(A[i,n]/A[n,n])*b[n]
        A[i]=A[i]-(A[i,n]/A[n,n])*A[n]
          
  
A=array([[1.,2.,3.],[3.,2.,2.],[2.,6.,2.]])
#b=array([3.,4.,4.])
b=array([[3.,4.],[4.,3.],[4.,5.]])
  
#row_reduce(A,b,1)
#print(A)
#print(b)
  
def pivot(A,b,n):
    N=len(b)
    eps=5*10**(-10) # a small number to verify the problem better than 0 
    if max(abs(A[n:N,n]))<eps:
        raise Exception('A is noninvertible')
         
    M=argmax(abs(A[n:N,n]))+n
    #argmax can output the index of the largest row
    #A[n:N,n] is a new matrix
      
    if M!=n :
        Acopy=A[n].copy()
        A[n]=A[M]
        A[M]=Acopy
        bcopy=b[n].copy()
        b[n]=b[M]
        b[M]=bcopy
          
      
  
     
  
#pivot(A,b,1)
#print(A)
#print(b)
  
def gauss_eliminate(A,b):
    #b can be a N*M matrix
    Acopy=A.copy()
    bcopy=b.copy()
    #print(b.ndim)
    #nshape=b.shape
    #print(nshape)
    n=len(b)
    for i in range(n):
        pivot(Acopy,bcopy,i)
        row_reduce(Acopy,bcopy,i)
        
    if b.ndim==1:
        x=zeros(len(b))
    else:
        x=zeros(b.shape)
    
    for i in range(n-1,-1,-1):
        u = bcopy[i]  #do need to define u before use it
        v = dot(Acopy[i,i+1: n],x[i+1:n])  #matrix multiplication
        w = u-v
        x[i]=w/Acopy[i,i]  #need to define x before use it
        #x[i]=(bcopy[i]-dot(Acopy[i,i+1: n],x[i+1:n]))/Acopy[i,i]
        
    return x
  
#print(gauss_eliminate(A,b))
#print(A)
#print(b)
 

 
def gauss_eliminate_profile(A,b):
    TN=zeros(20) #test 10 times
    TN1=zeros(20)
    N=array([10,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475])
     
    for i in range(20):
       A=random.uniform(low=0.5,high=100.,size=(N[i],N[i]))
       b=random.uniform(low=0.5,high=100,size=N[i])
       #print(A)
       #print(b)
       start=time.perf_counter()
       gauss_eliminate(A,b)
       TN[i]=time.perf_counter()-start
       start1=time.perf_counter()
       scipy.linalg.solve(A,b)
       TN1[i]=time.perf_counter()-start1
 
    x1=polyfit(log(N),log(TN),1)
    x2=polyfit(log(N[4:]),log(TN1[4:]),1)
    # start from N=100 for linalg.solve function time
    plt.loglog(N,TN,'r--',label='my own,q=%.5f'%x1[0])
    plt.loglog(N,TN1,'b',label='python own,q=%.5f'%x2[0])
    plt.legend()  #legend
     
    plt.show()
 
    return TN,TN1
  
#print(gauss_eliminate_profile(A,b))
# start from N=100 for linalg.solve function time
#the p means the order of time, while the q is the parameter before it.
 

#test the speed of matrix inversion
def gauss_eliminate_profile2():
    TN=zeros(20) #test 10 times
    TN1=zeros(20)
    N=array([10,25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475])
     
    for i in range(20):
       A=random.uniform(low=0.5,high=100.,size=(N[i],N[i]))
       b=zeros((N[i],N[i]))
       for j in range(N[i]):
           b[j,j]=1
           
       #print(A)
       #print(b)
       start=time.perf_counter()
       gauss_eliminate(A,b)
       TN[i]=time.perf_counter()-start
       start1=time.perf_counter()
       scipy.linalg.inv(A)
       TN1[i]=time.perf_counter()-start1
 
    x1=polyfit(log(N),log(TN),1)
    x2=polyfit(log(N[4:]),log(TN1[4:]),1)
    # start from N=100 for linalg.solve function time
    plt.loglog(N,TN,'r--',label='my own,q=%.5f'%x1[0])
    plt.loglog(N,TN1,'b',label='python ,q=%.5f'%x2[0])
    plt.legend()  #legend
     
    plt.show()
 
    return TN,TN1
    
gauss_eliminate_profile2()

    
