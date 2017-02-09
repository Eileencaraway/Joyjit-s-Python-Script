from scipy import *

a=arange(60.).reshape((5,3,4))
b=arange(24.).reshape((4,3,2))
c=tensordot(a,b,axes=2)
print(c.shape)
