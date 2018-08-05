#!/bin/bash 

datadir=/home/anael/data/shear2
for size in 40 ;
do 
    mkdir -p results/pf-0.90/size-${size}
    for gdot in 0.0001 0.001 0.01 ;
    do
    echo ${datadir}/pf-0.90/size-${size}

    ~/research/mols/test/analyze 1 4 shear-eta-5-gdot-${gdot}-g- ${datadir}/pf-0.90/size-${size}/sys-000
    \mv gr results/pf-0.90/size-${size}/shear-eta-5-gdot-${gdot}-g-4.res
    done
done

