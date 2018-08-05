#!/bin/bash

if [ $# -lt 1 ] ;
    then 
    echo "# Usage: directory lists "
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

#####################################
## extracting chemical potential value from mcgibbsmix.out:
cud=$PWD
echo $cud
 
for d in ${dir[*]} ; 
do 
    cd $d ; 
    pwd ; 
    
    tail -15 mcgibbsmix.out > look

    # reading chemical potentials of Subsystem 0 
    str0=$(sed -n '6p' look) ;
    let j="0"  
    for s in $str0 ; 
    do 
	cp0[$j]=$s ; 
	j=$[$j+1] ;
    done
    echo ${cp0[2]};
    echo ${cp0[3]};
	
    # reading chemical potentials of Subsystem 1 
    str1=$(sed -n '12p' look) ;
    let j="0"  
    for s in $str1 ; 
    do 
	cp1[$j]=$s ; 
	j=$[$j+1] ;
    done
    echo ${cp1[2]};	
    echo ${cp1[3]};
	
    rm -rf look 
	
    out=''
    ch4=$(echo ${cp0[2]} '> ' ${cp1[2]} | bc) ; # return 1 if true, else return 0
    if [ $ch4 -eq 1 ] ; 
    then
	#echo 'Sub 0'
	out=$out${cp0[2]}'      '${cp1[2]}
    else
	#echo 'Sub 1'
	out=$out${cp1[2]}'      '${cp0[2]}

    fi

    out=$out'      '
    cf4=$(echo ${cp0[3]} '> ' ${cp1[3]} | bc) ; # return 1 if true, else return 0
    if [ $cf4 -eq 1 ] ; 
    then
	#echo 'Sub 0'
	out=$out${cp0[3]}'      '${cp1[3]}
    else
	#echo 'Sub 1'
	out=$out${cp1[3]}'      '${cp0[3]}

    fi
    
    file='chemPot.dat';
    echo "writing .. "$file
    echo "#   CH4            CF4" > $file
    echo "# H      L      H      L" >> $file
    echo $out >> $file
    
    echo $d':  job is done'
    cd $cud ; 
done

#####################################
## Averaging over all directories:
file='chemPot.dat';
avgfile='avg_chemPot.dat'
echo "writing .. "$avgfile

str=' '
for d in ${dir[*]} ; 
do 
    str=$str$d'/'$file' '
done

avg_line.py $str > $avgfile ; 


