from scipy import *
import matplotlib.pyplot as plt
  
##plot the picture in 2D space, x,y describe the space.
##A is a 1D array made of complex number 
##kvector is 3*N matrix, N is the same with A's len
##Psi is a 2D array of the same size of x,y, made of complex number
## J/j can be used directly to say a number is complex number
  
def wave_superposition(x, y, Amplitudes, Kvectors):
    assert len(x) == len(y)
    # assert len(Amplitudes) == len(Kvectors[:,0])
    N=len(Amplitudes)
    phi=zeros(x.shape, dtype=complex)  # tell this one it is a complex number
    for i in range(N):
        phi+=Amplitudes[i]*exp(1j*(Kvectors[i,0]*x+Kvectors[i,1]*y)) #matric can be used directly
    return phi
          
  
x,y=array([[1.0,2.0],[1.0,3.0]]), array([[2.0,4.0],[2.0,4.0]]) #use tuple, we need to say array 
  
k=array([[1.0,-1.0]]) #two [] to make it a 2D vector
  
A= array([1.0+0j])  #A is a complex number, just put complex number inside?
                 #r is a matric? r= array([x,y])
psi= wave_superposition(x,y,A,k)
print(psi)
