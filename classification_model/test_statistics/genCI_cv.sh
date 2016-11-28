#! /bin/bash

dir=/scratch/garyli/database/test_stats_192urs/
cd $dir


if [ ! -f /scratch/garyli/database/test_stats_192urs/bootaucs_calci.py ]; then
        ln -s /home/garyli/scripts/cho/bootaucs_calci.py .
else
        echo bootaucs_calci.py exist
fi


#for l in $dir/*.ts
#do
#base=`basename $l .im`
#parts=(`echo $base | tr '.' ' '`)
 #if [ "${parts[3]}" == "cp30" ]; then
#	echo $l
       # ./bootaucs_CI.py 500 90 $base.bs.aucs.ci90 $l >> confidence_intervals_90p.txt 2>&1 &  
#	./bootaucs_CI.py 500 95 $base.bs.aucs.ci95 $l >> confidence_intervals_95p.txt 2>&1 & 
 #fi
#done

args=("$@")
if [ $# -ne 1 ]; then
        echo "Usage: genaucs_n_cis.sh cutoff_frequency"
        exit
fi
cf=${args[0]}

#c=30
for a in 00
do
for p in 10 50 90
do 
for cl in 25 50 75 100 125 150
do 
#ls -l a$a.hp$hp.cl$cl.c18.cp30.ts
./bootaucs_CI.py 200 95 a$a.hp$p.cl$cl.c$cf.boot.aucs.ci95 a$a.hp$p.cl$cl.c$cf.ts >> confidence_intervals_95p_a$a.txt 2>&1 & 

done
done
done
