import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy import *

import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

class ParticleBox:
    """Orbits class

    init_state is an [N x 6] array, where N is the number of particles:
       [[x1, y1, vx1, vy1,fx1,fy1],
        [x2, y2, vx2, vy2,fx2,fy2],
        ...               ]

    bounds is the size of the box: [xmin, xmax, ymin, ymax]
    """
    def __init__(self,
                 init_state = [[1, 0, 0, -1,0,0],
                               [-0.5, 0.5, 0.5, 0.5,0,0],
                               [-0.5, -0.5, -0.5, 0.5,0,0]],
                 bounds = [-2, 2, -2, 2],
                 size = 0.04,
                 M = 0.05,
                 G = 9.8,
                 k=1.,
                 e=1.,
                 sigma=.3):
                 # e and sigma are the parameter from lj potential
                 #how to decide these parameters?
        self.init_state = np.asarray(init_state, dtype=float)
        self.M = M * np.ones(self.init_state.shape[0])
        self.size = size
        self.state = self.init_state[:,:4].copy()
        self.time_elapsed = 0
        self.bounds = bounds
        self.G = G
        self.force=self.init_state[:,4:].copy()
        #self.force is a N*2 matrix, store the force on x,y direction of each particles
    def init_force(self):
        k=1.
        e=1.
        sigma=.3

        n,m=self.state.shape
        #n=len(init_state[:,0])

        for i in range(n):
            xi=self.state[i,0]
            yi=self.state[i,1]
            lj_x=0.
            lj_y=0.
            for j in range(n):
                if j!=i:
                    xj,yj=self.state[j,0],self.state[j,1]
                    rij=sqrt((xi-xj)**2+(yi-yj)**2)
                    #force origin from lj part
                    lj_x+=24*e*((2/rij)*(sigma/rij)**12-(1/rij)*(sigma/rij)**6)*((xi-xj)/rij)
                    lj_y+=24*e*((2/rij)*(sigma/rij)**12-(1/rij)*(sigma/rij)**6)*((yi-yj)/rij)

            #self.force[i,0]=-k*self.state[i,0]+lj_x
            self.force[i,0]=lj_x
            #self.force[i,1]=-k*self.state[i,1]+lj_y
            self.force[i,1]=lj_y

        print(self.force)


    def step(self, dt):

        """step once by dt seconds"""
        self.time_elapsed += dt
        #MM is the mass of one particle
        MM=0.05
        k=1.
        e=1.
        sigma=.3
        n,m=self.state.shape
        #count=0
        #global count
        #count =0
        #not very sure about the usage of global variable


        #force is from the calculation before this step
        #start from init_state
        #temporary velocity
        self.state[:,2:]+=0.5*dt*self.force[:,:]/MM

        # update positions
        self.state[:, :2] += dt * self.state[:, 2:]

        print(self.state[:,:])

        '''# find pairs of particles undergoing a collision
        D = squareform(pdist(self.state[:, :2]))
        ind1, ind2 = np.where(D < 2 * self.size)
        unique = (ind1 < ind2)
        ind1 = ind1[unique]
        ind2 = ind2[unique]

        # update velocities of colliding pairs
        for i1, i2 in zip(ind1, ind2):
            # mass
            m1 = self.M[i1]
            m2 = self.M[i2]

            # location vector
            r1 = self.state[i1, :2]
            r2 = self.state[i2, :2]

            # velocity vector
            v1 = self.state[i1, 2:]
            v2 = self.state[i2, 2:]

            # relative location & velocity vectors
            r_rel = r1 - r2
            v_rel = v1 - v2

            # momentum vector of the center of mass
            v_cm = (m1 * v1 + m2 * v2) / (m1 + m2)

            # collisions of spheres reflect v_rel over r_rel
            rr_rel = np.dot(r_rel, r_rel)
            vr_rel = np.dot(v_rel, r_rel)
            v_rel = 2 * r_rel * vr_rel / rr_rel - v_rel

            # assign new velocities
            self.state[i1, 2:] = v_cm + v_rel * m2 / (m1 + m2)
            self.state[i2, 2:] = v_cm - v_rel * m1 / (m1 + m2)'''

        # check for crossing boundary
        crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.size)
        crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.size)
        crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.size)
        crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.size)

        self.state[crossed_x1, 0] = self.bounds[0] + self.size
        self.state[crossed_x2, 0] = self.bounds[1] - self.size

        self.state[crossed_y1, 1] = self.bounds[2] + self.size
        self.state[crossed_y2, 1] = self.bounds[3] - self.size

        self.state[crossed_x1 | crossed_x2, 2] *= -1
        self.state[crossed_y1 | crossed_y2, 3] *= -1

        #update velocity
        #force after verlet algorithm
        for i in range(n):
            xi,yi=self.state[i,0],self.state[i,1]
            lj_x=0
            lj_y=0
            for j in range(n):
                if j!=i:
                    xj,yj=self.state[j,0],self.state[j,1]
                    rij=sqrt((xi-xj)**2+(yi-yj)**2)
                    #force origin from lj part
                    lj_x+=24*e*((2/rij)*(sigma/rij)**12-(1/rij)*(sigma/rij)**6)*((xi-xj)/rij)
                    lj_y+=24*e*((2/rij)*(sigma/rij)**12-(1/rij)*(sigma/rij)**6)*((yi-yj)/rij)

            #self.force[i,0]=-k*self.state[i,0]+lj_x
            self.force[i,0]=lj_x
            #self.force[i,1]=-k*self.state[i,1]+lj_y
            self.force[i,1]=lj_y
        print(self.force)

        self.state[:,2:]+=0.5*dt*self.force[:,:]/MM

np.random.seed(0)
init_state = -0.5 + np.random.random((10, 6))

init_state[:, :2] *= 3.9
init_state[:,2:]*=30

box = ParticleBox(init_state, size=0.04)
dt = 1. / 1000# 30fps
box.init_force()

fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
#ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                    # xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))

for i in range(500):
    box.step(dt)

    # update pieces of the animation
    #rect.set_edgecolor('k')
    #particles.set_data(box.state[:, 0], box.state[:, 1])

    #particles.set_markersize(0.2)

    #fig=plt.figure()
    plt.plot(box.state[:,0],box.state[:,1],'bo')
    plt.xlim([-2.,2.])
    plt.ylim([-2.,2.])
    plt.savefig('frame%d.jpg'%i)
    plt.clf()
