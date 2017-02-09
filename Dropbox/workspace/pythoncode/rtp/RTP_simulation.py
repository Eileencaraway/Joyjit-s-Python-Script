import numpy as np
from scipy import *
from matplotlib import pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
#fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
#ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
#                     xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))
ax = fig.add_subplot(1,1,1)



def run_and_tumble(N=100000):
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
    return walkr


p=run_and_tumble()
#print(position)

# initialization function: plot the background of each frame
'''def init():
    global p
    line.set_data(0., 0.)
    return line,'''

# animation function.  This is called sequentially
def animate(i):
    global p
    x=p[i,0]
    y=p[i,1]
    ax.plot(x,y)

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate,
                                interval=100)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
