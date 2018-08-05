#! /usr/bin/env python

import sys
from numpy import *
from pylab import *
import os
import StringIO
from math import pi, atan2, sin, cos, sqrt, floor, exp

fd = open(sys.argv[1],'rb')

colnb = fromfile(fd, int32, 1)[0]
print colnb

data = fromfile(fd, float32)
linenb = int(size(data)/colnb)

data.resize(linenb, colnb)
data = data.transpose()

plot(data[0],data[3])

show()


