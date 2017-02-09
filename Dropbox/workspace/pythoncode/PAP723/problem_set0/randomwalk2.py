import scipy 
import matplotlib.pyplot as plt
import turtle

turtle.speed('slowest')

def stepfun():
    x= array([[0.0,0.0],[1.0,0.0],[-1.0,0.0],[1.0,1.0],[-1.0,1.0],[1.0,-1.0],[-1.0,-1.0],[0.0,-1.0],[0.0,1.0]])
    return x[random.randint(0,9)]

# r size is  1*2
# walkr size is n*2
def random_walk_plot(stepfun,nsteps):
    r=[0,0]
    walkr=r
    for i in range(nsteps):
        r+=stepfun()
        
    walkr.append(r)
    print(walkr)

    plt.plot(walk[:,0],walk[:,1])
    plt.axis(-10,10,-10,10)
    plt.show()
   


