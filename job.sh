#!/bin/bash

if [ $# -lt 1 ] ;
    then 
    echo "# Usage: args ... "
    exit
fi
 
#####################################
## Readig arguments :
echo "# No. of arguments given is "$#

let i="0"  
for a in $* ; 
do 
    dir[$i]=$a ; 
    i=$[$i+1] ;
done

echo "# Following arguments are found: "
echo ${dir[*]} ; 
