#! /bin/bash

age=$1
alpha=$2
count_level=$3
cf=$4

if [ $# -ne 4 ]
    then
        echo "Arguments: age alpha count_level cutoff(# after digit)"
        exit 1
fi

for c in $count_level 
do
for p in 10 50 90
 do
 for a in $alpha 
  do
 #echo ${a:2}
  #echo ${a:2}
  # echo a${age}.hp${p}.cl$c.c$cf.ts $a a${age}.hp${p}.cl$c.c$cf.alpha${a}.ts
  ./addInternalNoise.py a${age}.hp${p}.cl$c.c$cf.ts $a a${age}.hp${p}.cl$c.c$cf.alpha${a}.ts
  done
done
done
