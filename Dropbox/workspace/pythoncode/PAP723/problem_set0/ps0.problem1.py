from scipy import *
import matplotlib.pyplot as plt

##A is a 1D array made of complex number
##kvector is 2*N matrix, N is the same with A's length
##Psi is a 2D array of the same size of x,y, made of complex number

def wave_superposition(x, y, Amplitudes, Kvectors):
    #assert len(x) == len(y)
    assert x.shape == y.shape
    assert len(Amplitudes) == len(Kvectors[:,0])
    N=len(Amplitudes)
    phi=zeros(x.shape, dtype=complex)  # tell this one it is a complex number
    for i in range(N):
        phi+=Amplitudes[i]*exp(1j*(Kvectors[i,0]*x+Kvectors[i,1]*y))
        #matric can be used directly
        #J/j can be used directly to say a number is complex number
    return phi
    #phi is the same shape as X, Y
    #return the phi at each point of x,y
    #the sum is superposition of N plane waves



##plot the picture in 2D space, x,y describe the space.
def interference_xy_plot(xspan,yspan,amplitudes,kvectors):
    xmin, xmax, N2 = xspan
    ymin, ymax, M2 = yspan  # use tuple to give it value
    x=linspace(xmin,xmax,N2)
    y=linspace(ymin,ymax,M2)
    X,Y=meshgrid(x,y) #X is a matrix contain all the x value of grids
    phi=wave_superposition(X,Y,amplitudes,kvectors)
    # phi is the same shape as X
    #print(phi)
    plt.subplot(1,2,1)
    label_1="plot of intensity"
    label_2="plot of phase"
    plt.pcolormesh(X,Y,(abs(phi))**2, cmap='RdBu',label=label_1) #
    plt.title('Intensity')
    plt.xlabel('X')
    plt.ylabel('Y')
    #plt.axis([x.min(),x.max(),y.min(),y.max()])
    plt.colorbar()

    plt.subplot(1,2,2)
    plt.pcolormesh(X,Y,angle(phi),cmap='RdBu',label=label_2)
    plt.title('phase')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.colorbar()
    plt.show()


def interference_demo(k0=1.0):
    xasy=(0,50,500)
    yasy=(0,50,500)
    k=array([[k0,0],[-k0*cos(pi/3),k0*sin(pi/3)],[-k0*cos(pi/3),-k0*sin(pi/3)]])
    A= array([[1.],[1.],[1.]])
    interference_xy_plot(xasy,yasy,A,k)
##you can see clearly the pattern of Intensity
##The thing to notice about the numerical plots is that there is a
##phase singularity (vortex) at each intensity minimum (node).
interference_demo(0.125)
#in the phase picture,we can realize the maximum points are in the mid of each hexagon
#It is easier to decide antinotes from Intensity plot.
#the minimum points are the vertex of the hexagon.
#the antinotes(max) are (0,0),(33.0,0),(16.7,29.0),(16.7,29.0)
#the notes(min) are (only list six clorkwise circle around(16.7,29.0)):
#(16.7,9.7),(0,19.3),(0,38.7),(16.7,48.3)(33.5,38.7),(33.5,19.3)
