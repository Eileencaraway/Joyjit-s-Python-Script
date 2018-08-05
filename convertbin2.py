#! /usr/bin/env python

import sys
from numpy import *
from pylab import *
import os
import StringIO
from math import pi, atan2, sin, cos, sqrt, floor, exp
import struct

fd = open(sys.argv[1],'rb')

data = fromfile(fd, float32)

ival = struct.pack('i',9)

out = open(sys.argv[2],'wb')
out.write(ival)
out.write(data)

#show()


