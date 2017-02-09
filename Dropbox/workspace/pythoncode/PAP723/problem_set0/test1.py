from scipy import *
import matplotlib.pyplot as plt
import pylab as P

mu, sigma = 200, 25
x = mu + sigma*P.randn(10000)

# the histogram of the data with histtype='step'
n, bins, patches = P.hist(x, 50, normed=1, histtype='stepfilled')
P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)

# add a line showing the expected distribution
y = P.normpdf( bins, mu, sigma)
l = P.plot(bins, y, 'k--', linewidth=1.5)


#
# create a histogram by providing the bin edges (unequally spaced)
#
P.figure()
