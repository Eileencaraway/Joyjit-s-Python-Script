#! /usr/bin/env python

from numpy import *

def readData(filename):
    file = open(filename)
    data = []
    header = []
    for line in file:
        c = line.split()[0][0]
        if c=="#" or c=="&":
            header.append(line)
        else:
            data.append(fromstring(line,sep=" "))
    file.close()
    return [data, header]


class DataCollector:
    def __init__(self, xmin, xmax, computeErrors=True):
        self.M = empty(0)
        self.M2 = empty(0)
        self.first = True
        self.Ninst = 0
        self.means = []
        self.mean2s = []
        self.xmin = xmin
        self.computeErrors = computeErrors

    def collect(self, data):

        if self.first:
            self.first = False
            A = array(data)
            A2 = A*A

            self.M  = A
            if self.computeErrors:
                self.M2 = A2
            self.Ninst = 1

            i0 = less(self.xmin,A[:,0])
            self.means.append(mean(A[i0,:],axis=0))
            self.mean2s.append(mean(A2[i0,:],axis=0))
        else:
            if len(data) == size(self.M,0):
                A = array(data)
                A2 = A*A

                self.M  += A
                if self.computeErrors:
                    self.M2 += A2
                self.Ninst += 1

                i0 = less(self.xmin,A[:,0])
                self.means.append(mean(A[i0,:],axis=0))
                self.mean2s.append(mean(A2[i0,:],axis=0))


    def finalize(self):
        self.M  /= self.Ninst
        if self.computeErrors:
            self.M2 /= self.Ninst
            self.M2 -= self.M*self.M
        self.means = array(self.means)
        self.mean2s = array(self.mean2s)
        self.mean2s -= self.means*self.means
