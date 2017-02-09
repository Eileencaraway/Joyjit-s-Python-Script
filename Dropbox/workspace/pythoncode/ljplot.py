from scipy import *
import matplotlib.pyplot as plt

e=1.0
sigma=1.0

def ljpotential(r):
    return 4*e*((sigma/r)**12-(sigma/r)**6)

def force(r):
    return 24*e*((2/r)*(sigma/r)**12-(1/r)*(sigma/r)**6)

d=linspace(0.8,3,10000)
#when the range is not good
#the detail of the plot cannot show
U=zeros(len(d))
F=zeros(len(d))

for i in range(len(d)):
    U[i]=ljpotential(d[i])
    F[i]=force(d[i])

plt.subplot(211)
plt.ylim(-2,5)
plt.plot(d,U)
plt.ylabel('Potential')
plt.subplot(212)
plt.ylim(-10,20)
plt.plot(d,F)
plt.ylabel('Force')

plt.show()
print(ljpotential(1.120))
print(ljpotential(0.5))
