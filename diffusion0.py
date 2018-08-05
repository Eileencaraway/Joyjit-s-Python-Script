#! /usr/bin/env python

import sys
import os

temperaturelist = [ 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6 ]
gdotlist = [ 0.01, 0.004, 0.001, 0.0004, 0.0001, 4e-05, 1e-05 ]

                    
temperaturefile = {}
for temperature in temperaturelist:
#    filename = 'res.difftemperature-'+str(temperature)+'-18.dif'
    filename = 'res.difftemperature-'+str(temperature)
    temperaturefile[temperature] = open(filename, 'w')

    
gdotfile = {}
for gdot in gdotlist:
#    filename = 'res.diffgdot-'+str(gdot)+'-18.dif'
    filename = 'res.diffgdot-'+str(gdot)
    gdotfile[gdot] = open(filename, 'w')



for temperature in temperaturelist:
    for gdot in gdotlist:
        filename = 'shear-T-'+str(temperature)+'-gdot-'+str(gdot)+'-g-13.dif4'
        #filename = 'shear-T-'+str(temperature)+'-gdot-'+str(gdot)+'-g-18.dif4'

        n =0
        while n <= 9:
            if os.path.exists('sys-00'+str(n)+'/'+filename):
                print filename, 'exists'
                os.system('~/pythontest/avg_cutoff-diff.py sys-*/'+filename+ '>look')
                file = open('look')
                data = file.readlines()
                
                if len(data)> 0:
                    vals = data[len(data)-1].split() 
                    
                    if len(vals) > 4:
                        print >>gdotfile[gdot], temperature, 
                        print >>temperaturefile[temperature], gdot, 
                        
                    for i in range(6, len(vals)):
                        print >>gdotfile[gdot], vals[i],
                        print >>temperaturefile[temperature], vals[i],
                        
                    print >>gdotfile[gdot]
                    print >>temperaturefile[temperature]
                
                n = 9
                
            n += 1

 
