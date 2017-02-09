from scipy import *
import matplotlib.pyplot as plt
from matplotlib import animation

## stepfun is a function can randomly produce 2D output inside of my choice at every time when I call it
def stepfun1():
    x= array([[0.0,0.0],[1.0,0.0],[-1.0,0.0],[1.0,1.0],[-1.0,1.0],[1.0,-1.0],[-1.0,-1.0],[0.0,-1.0],[0.0,1.0]])
    return x[random.randint(0,9)]


##random_walk_plot try to animate the process, can use animation function or turtle
##r stands for the vector of the particle. 
def random_walk_plot(stepfun,nsteps):
    fig=plt.figure()
    ax=plt.axes(xlim=(0, nsteps),ylim=(0,nsteps))
    line, = ax.plot([],[],lw=2)
    def init():
        line.set_data([],[])
        return line,
    def stepfun1():
        x= array([[0.0,0.0],[1.0,0.0],[-1.0,0.0],[1.0,1.0],[-1.0,1.0],[1.0,-1.0],[-1.0,-1.0],[0.0,-1.0],[0.0,1.0]])
        return x[random.randint(0,9)]
    #x=linspace(0,nsteps,nsteps+1)
    #y=linspace(0,nsteps,nsteps+1)
    #X,Y=meshgrid(x,y)
    r=array([nsteps/2,nsteps/2])
    def animate():
        r+=stepfun1()
        line.set_data(r[0],r[1])
        return line,
    
    anim= animation.FuncAnimation(fig,animate,init_func=init,frames=100,interval=20,blit=True)
    

random_walk_plot(stepfun1, 100)
