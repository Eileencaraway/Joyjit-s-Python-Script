#! /usr/bin/env python

import sys
from numpy import *
from pylab import *
import os
import StringIO
from math import pi, atan2, sin, cos, sqrt, floor, exp

fd = open(sys.argv[1],'rb')

data = fromfile(fd, float32)

lines_nb = size(data)/11

data = reshape(data,(-1, 11))

plot(data[0],data[3])

for line in data:
    for val in line:
        print val,
    print

show()


