#!/usr/bin/env python

import sys
import os
import StringIO
import math
import numpy
from numpy import *
#from matplotlib import *
#from pylab import show 

class Histogram:
    
    def __init__(self, _a=0.0, _b=10.0, _N=1000):
        self.a  = _a
        self.b  = _b
        self.N  = _N
        self.dx = (self.b-self.a)/self.N
        self.one_over_dx = 1/self.dx
        self.n = arange(self.a,self.b,self.dx)
        for i in range(len(self.n)):
            self.n[i]=0
        
        self.dtpoints_nb =0
        self.dtpoints_nbob =0    # data points out of bound
        self.rho = arange(self.a,self.b,self.dx)


    def reset(self):
        for i in range(len(self.n)):
            self.n[i]=0
            self.rho[i] = 0

        self.dtpoints_nb = 0
        self.dtpoints_nbob = 0
        return 0
            

    def store(self, x):
        bin = math.floor(self.one_over_dx * (x-self.a))
        
        if (int(bin)>=0 and int(bin)<self.N) :
            self.n[bin] +=1
        else:
            self.dtpoints_nbob +=1

        self.dtpoints_nb +=1
        return 0
        

    def storeVal(self, x, y):
        bin = math.floor(self.one_over_dx * (x-self.a))
        
        if (int(bin)>=0 and int(bin)<self.N) :
            self.n[bin] += y
            
        self.dtpoints_nb +=1
        return 0
        

    def x(self, i):
        return self.a+(i+0.5)*self.dx
        

    def normalize(self, coeff):
        if coeff == 0:
            coeff = self.one_over_dx/self.dtpoints_nb
        for i in range(len(self.n)):
            self.rho[i] = coeff*self.n[i]
            
        nb_points = self.dtpoints_nb
        self.dtpoints_nb =0
        return nb_points


    def getNbOb(self):
        return self.dtpoints_nbob


    def show(self):
        for i in range(len(self.n)):
            print self.x(i), " ",  self.rho[i]
        
        return 0


    def write(self, fname):
        fo = open(fname, 'w')
        for i in range(len(self.n)):
             print >> fo, self.x(i), " ",  self.n[i], " ", self.rho[i]

        fo.close()
        return 0



class Histogram2D:
    
    def __init__(self, _a=[0.0,0.0], _b=[10.0,10.0], _N=[1000,1000]):
        self.a  = list(_a)
        self.b  = list(_b)
        self.N  = list(_N)
        self.dx = [(self.b[d]-self.a[d])/self.N[d] for d in range(2)]
        self.one_over_dx   = [1.0/self.dx[d] for d in range(2)]
        self.n             = zeros(_N)
        self.dtpoints_nb   =0
        self.dtpoints_nbob =0    # data points out of bound
        self.rho = zeros(_N)


    def reset(self):
        self.n = zeros(self.N)
        self.rho = zeros(self.N)
        self.dtpoints_nb = 0
        self.dtpoints_nbob = 0
        return 0
            

    def store(self, x):
        bin = [math.floor(self.one_over_dx[d] * (x[d]-self.a[d])) for d in range(2)]
        
        if (int(bin[0])>=0 and int(bin[0])<self.N[0]) and (int(bin[1])>=0 and int(bin[1])<self.N[1]):
            self.n[bin[0]][bin[1]] +=1
        else:
            self.dtpoints_nbob +=1

        self.dtpoints_nb +=1
        return 0
        
    def normalize(self, coeff):
        if coeff==0:
            #coeff = self.one_over_dx/self.dtpoints_nb
            coeff = 1.0/self.dtpoints_nb

        for i in range(len(self.n[0])):
            for j in range(len(self.n[1])):
                self.rho[i][j] = coeff*self.n[i][j]
            
        nb_points = self.dtpoints_nb
        self.dtpoints_nb =0
        return nb_points
