#!/bin/bash

declare -a array=('TEMP' 'PRESS' 'NMOL' 'NCH4' 'NCF4' 'MASS' 'VOL' 'MDENSITY' 'NDENSITY' 'EPOT');
echo ${#array[@]} #Number of elements in the array

if [ $# -lt 1 ] ;
    then 
    echo "# Usage: T or P,  directory lists "
    exit
fi
 
#####################################
## Readig arguments :
echo "# No. of arguments given is "$#

let i="0"  
for a in $* ; 
do 
    if [ $i -lt 1 ] ; 
    then
	parm=$a ;
    else
	dir[$i]=$a ; 
    fi
    i=$[$i+1] ;
done

echo "# Following arguments are found: "
echo $parm ; 
echo ${dir[*]} ; 

#####################################
## Operating the script analyzeMCmix.py:
cud=$PWD
echo $cud
 
for d in ${dir[*]} ; 
do 
    cd $d ; 
    pwd ; 

    let var="2"
    while [ $var -lt ${#array[@]} ] ;
    do
	# reading values of the variable of Subsystem 0 
	analyzeMCmix.py -d 200000 -sub 0 mcgibbsmix.out $var > look0 ;  
	str0=$(tail -1 look0) ;
	let j="0"  
	for s in $str0 ; 
	do 
	    nbar0[$j]=$s ; 
	    j=$[$j+1] ;
	done
	# echo ${nbar0[6]}
	
	# reading values of the variable of Subsystem 1 
	analyzeMCmix.py -d 200000 -sub 1 mcgibbsmix.out $var > look1 ;
	str1=$(tail -1 look1) ;
	let j="0"  
	for s in $str1 ; 
	do 
	    nbar1[$j]=$s ; 
	    j=$[$j+1] ;
	done
	#echo ${nbar1[6]}
	
	
	file=${array[$var]}'.dat';
	echo "writing .. "$file
	
	nb=$(echo ${nbar0[6]} '> ' ${nbar1[6]} | bc) ; # return 1 if true, else return 0
	if [ $nb -eq 1 ] ; 
	then
	# echo 'Sub 0'
	    mv look0 $file
	    rm -rf look1
	else
	# echo 'Sub 1'
	    mv look1 $file
	    rm -rf look0
	fi
	
	var=$[$var+1] ;
    done 
    
    echo $d':  job is done'
    cd $cud ; 
done

#####################################
## Averaging over all directories:
let var="2"
while [ $var -lt ${#array[@]} ] ;
do
    file=${array[$var]}'.dat';
    avgfile='avg_'$file
    echo "writing .. "$avgfile
    
    str=' '
    for d in ${dir[*]} ; 
    do 
	str=$str$d'/'$file' '
    done

    avg_cutoff.py -set 200000 10000000000 $str > $avgfile ; 

    var=$[$var+1] ;
done 